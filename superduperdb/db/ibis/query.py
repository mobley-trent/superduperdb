import dataclasses as dc
import enum
import random
import typing as t

from superduperdb import CFG
from superduperdb.container.document import Document
from superduperdb.db.ibis.cursor import SuperDuperIbisCursor


class QueryType(enum.Enum):
    QUERY = 'query'
    ATTR = 'attr'


class Query:
    def __init__(
        self,
        name,
        type=QueryType.QUERY.value,
        args=[],
        kwargs={},
        sddb_kwargs={},
        connection_parent=False,
    ):
        self.name = name
        query = query_lookup.get(name, None)
        if query is None:
            self.query = PlaceHolderQuery(name)
        else:
            self.query = query(**sddb_kwargs)
        self.type = type
        self.args = args
        self.kwargs = kwargs
        self.connection_parent = connection_parent

    def execute(self, db, parent, table, ibis_table=None):
        if self.type == QueryType.ATTR.value:
            return getattr(parent, self.query.name)

        self.query.pre(db)
        if len(self.args) == 1 and isinstance(self.args[0], QueryLinker):
            self.args = [self.args[0].execute(db, parent, ibis_table)]

        if self.query.namespace == 'ibis':
            if self.connection_parent:
                parent = getattr(db.db, self.query.name)(*self.args, **self.kwargs)
            else:
                parent = getattr(parent, self.query.name)(*self.args, **self.kwargs)

        parent = self.query.post(
            db,
            parent,
            table=table,
            ibis_table=ibis_table,
            args=self.args,
            kwargs=self.kwargs,
        )
        return parent


class QueryChain:
    def __init__(self, seed=None, type=QueryType.QUERY.value):
        if isinstance(seed, str):
            query = Query(seed, type=type)
        elif isinstance(seed, Query):
            query = seed
        else:
            query = None

        self.chain = [query]

    def append(self, data, type=QueryType.QUERY.value):
        query = Query(data, type=type)
        self.chain.append(query)

    def append_query(self, query):
        self.chain.append(query)

    def get(self, ix):
        return self.chain[ix]

    def update_last_query(self, args, kwargs, type=None):
        self.chain[-1].args = args
        self.chain[-1].kwargs = kwargs
        if type:
            self.chain[-1].type = type

    def __iter__(self):
        for query in self.chain:
            if query.type in [QueryType.QUERY.value, QueryType.ATTR.value]:
                yield query


@dc.dataclass
class Table:
    name: str
    primary_id: str = 'id'

    def __getattr__(self, k):
        if k in self.__dict__:
            return self.__getattr__(k)
        return QueryLinker(
            self, query_type=k, members=QueryChain(k, type=QueryType.ATTR.value)
        )

    def like(self, r=None, n=10, vector_index=None):
        k = 'prelike'
        kwargs = {'r': r, 'n': n, 'vector_index': vector_index}
        query = Query(k, args=[], sddb_kwargs=kwargs)
        return QueryLinker(self, query_type=k, members=QueryChain(query))

    def insert(
        self,
        *args,
        refresh: bool = True,
        verbose: bool = True,
        encoders: t.Sequence = [],
        valid_prob: float = 0.05,
        **kwargs,
    ):
        sddb_kwargs = {
            'refresh': refresh,
            'verbose': verbose,
            'encoders': encoders,
            'kwargs': {'valid_prob': valid_prob},
            'documents': args[0],
        }
        args = args[1:]
        insert = Query(
            'insert',
            type=QueryType.QUERY.value,
            args=args,
            kwargs=kwargs,
            sddb_kwargs=sddb_kwargs,
            connection_parent=True,
        )

        qc = QueryChain(insert)
        return QueryLinker(self, query_type='insert', members=qc)


class LogicalExprMixin:
    def _logical_expr(self, other, members, collection, k):
        args = [other]
        members.append_query(Query(k, args=args, kwargs={}))
        return QueryLinker(collection, query_type=k, members=members)

    def eq(self, other, members, collection):
        k = '__eq__'
        return self._logical_expr(other, members, collection, k)

    def gt(self, other, members, collection):
        k = '__gt__'
        return self._logical_expr(other, members, collection, k)

    def lt(self, other, members, collection):
        k = '__lt__'
        return self._logical_expr(other, members, collection, k)


@dc.dataclass
class QueryLinker(LogicalExprMixin):
    collection: Table
    query_type: str = 'find'
    args: t.Sequence = dc.field(default_factory=list)
    kwargs: t.Dict = dc.field(default_factory=dict)
    members: QueryChain = dc.field(default_factory=QueryChain)

    def __getattr__(self, k):
        if k in self.__dict__:
            return self.__getattr__(k)
        self.members.append(k)
        return QueryLinker(self.collection, query_type=k, members=self.members)

    def __eq__(self, other):
        return self.eq(other, members=self.members, collection=self.collection)

    def __lt__(self, other):
        return self.lt(other, members=self.members, collection=self.collection)

    def __gt__(self, other):
        return self.gt(other, members=self.members, collection=self.collection)

    def select_ids(self):
        k = 'select'
        args = [self.collection.primary_id]
        self.members.append_query(Query(k, args=args, kwargs={}))
        return QueryLinker(self.collection, query_type='select', members=self.members)

    def select_from_ids(self, ids):
        isin_query = self.collection.__getattr__(self.collection.primary_id).isin(ids)
        k = 'filter'
        args = [isin_query]
        self.members.append_query(Query(k, args=args, kwargs={}))

        return QueryLinker(self.collection, query_type='filter', members=self.members)

    def __call__(self, *args, **kwargs):
        self.members.update_last_query(args, kwargs, type=QueryType.QUERY.value)

        return QueryLinker(
            collection=self.collection,
            query_type=self.query_type,
            members=self.members,
            args=args,
            kwargs=kwargs,
        )

    def execute(self, db, parent, ibis_table):
        for member in self.members:
            parent = member.execute(db, parent, self.collection, ibis_table=ibis_table)
        return parent


class IbisConnection:
    def __init__(self, db):
        self.db = db

    def _execute(self, db, query, parent):
        table = parent
        for member in query.members:
            parent = member.execute(
                db, parent, table=query.collection, ibis_table=table
            )
        cursor = SuperDuperIbisCursor(parent, query.collection.primary_id, encoders={})
        return cursor.execute()

    def execute(self, query):
        return self._execute(self.db, query, self.db.table(query.collection.name))


class PlaceHolderQuery:
    type_id: t.Literal['query'] = 'query'  # type: ignore[annotation-unchecked]

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs

        self.namespace: str = 'ibis'  # type: ignore[annotation-unchecked]

    def pre(self, db):
        ...

    def post(self, db, output, *args, **kwargs):
        return output


@dc.dataclass
class PostLike:
    type_id: t.Literal['Ibis.PostLike'] = 'Ibis.PostLike'
    name: str = 'postlike'
    namespace: str = 'sddb'

    def pre(self, db):
        pass

    def post(self, db, output, table=None, ibis_table=None, args=[], kwargs={}):
        r = kwargs.get('r', None)
        assert r is not None, 'r must be provided'
        n = kwargs.get('n', 10)

        vector_index = kwargs.get('vector_index', 'vector_index')
        ids = output.select(table.primary_id)
        ids, scores = db._select_nearest(
            like=r,
            vector_index=vector_index,
            n=n,
            ids=ids,
        )
        return output.filter(  # type: ignore[annotation-unchecked]
            ibis_table.__getattr__(table.primary_id).isin(ids)
        )


@dc.dataclass
class PreLike:
    r: t.Any
    vector_index: str = 'vector_index'
    n: int = 10
    collection: str = 'collection'
    primary_id: str = 'id'
    type_id: t.Literal['Ibis.PreLike'] = 'Ibis.PreLike'
    name: str = 'prelike'
    namespace: str = 'sddb'

    def pre(self, db):
        pass

    def post(self, db, output, table=None, ibis_table=None, args=[], kwargs={}):
        '''

        ids, _ = db._select_nearest(
            like=self.r, vector_index=self.vector_index, n=self.n
        )
        '''
        ids = [1, 2, 3]
        f = output.filter(ibis_table.__getattr__(self.primary_id).isin(ids))
        return f


@dc.dataclass
class Insert:
    documents: t.List['Document'] = dc.field(default_factory=list)
    refresh: bool = True
    verbose: bool = True
    kwargs: t.Dict = dc.field(default_factory=dict)
    encoders: t.Sequence = dc.field(default_factory=list)
    type_id: t.Literal['Ibis.insert'] = 'Ibis.insert'
    name: str = 'insert'
    namespace: str = 'ibis'

    def pre(self, db):
        valid_prob = self.kwargs.get('valid_prob', 0.05)

        for e in self.encoders:
            db.add(e)
        documents = [r.encode() for r in self.documents]
        for r in documents:
            if '_fold' in r:
                continue
            if random.random() < valid_prob:
                r['_fold'] = 'valid'
            else:
                r['_fold'] = 'train'

        return documents

    def post(self, db, output, *args, **kwargs):
        graph = None
        if self.refresh and not CFG.cdc:
            graph = db.refresh_after_update_or_insert(
                query=self,  # type: ignore[arg-type]
                ids=output.inserted_ids,
                verbose=self.verbose,
            )
        return graph, output


query_lookup = {'insert': Insert, 'prelike': PreLike, 'like': PostLike}
