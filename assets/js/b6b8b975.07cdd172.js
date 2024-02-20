"use strict";(self.webpackChunknewdocs=self.webpackChunknewdocs||[]).push([[419],{83189:(e,n,s)=>{s.r(n),s.d(n,{assets:()=>c,contentTitle:()=>t,default:()=>h,frontMatter:()=>i,metadata:()=>o,toc:()=>l});var d=s(85893),r=s(11151);const i={sidebar_position:19},t="Using AI APIs as Predictor descendants",o={id:"docs/walkthrough/ai_apis",title:"Using AI APIs as Predictor descendants",description:"In SuperDuperDB, developers are able to interact with popular AI API providers, in a way very similar to",source:"@site/content/docs/walkthrough/ai_apis.md",sourceDirName:"docs/walkthrough",slug:"/docs/walkthrough/ai_apis",permalink:"/docs/docs/walkthrough/ai_apis",draft:!1,unlisted:!1,editUrl:"https://github.com/SuperDuperDB/superduperdb/blob/main/docs/hr/content/docs/walkthrough/ai_apis.md",tags:[],version:"current",sidebarPosition:19,frontMatter:{sidebar_position:19}},c={},l=[{value:"OpenAI",id:"openai",level:2},{value:"Cohere",id:"cohere",level:2},{value:"Anthropic",id:"anthropic",level:2},{value:"Jina",id:"jina",level:2}];function a(e){const n={a:"a",code:"code",h1:"h1",h2:"h2",p:"p",pre:"pre",strong:"strong",table:"table",tbody:"tbody",td:"td",th:"th",thead:"thead",tr:"tr",...(0,r.a)(),...e.components};return(0,d.jsxs)(d.Fragment,{children:[(0,d.jsxs)(n.h1,{id:"using-ai-apis-as-predictor-descendants",children:["Using AI APIs as ",(0,d.jsx)(n.code,{children:"Predictor"})," descendants"]}),"\n",(0,d.jsxs)(n.p,{children:["In SuperDuperDB, developers are able to interact with popular AI API providers, in a way very similar to\n",(0,d.jsx)(n.a,{href:"/docs/docs/walkthrough/ai_models",children:"integrating with AI open-source or home-grown models"}),". Instantiating a model from\nthese providers is similar to instantiating a ",(0,d.jsx)(n.code,{children:"Model"}),":"]}),"\n",(0,d.jsx)(n.h2,{id:"openai",children:"OpenAI"}),"\n",(0,d.jsx)(n.p,{children:(0,d.jsx)(n.strong,{children:"Supported"})}),"\n",(0,d.jsxs)(n.table,{children:[(0,d.jsx)(n.thead,{children:(0,d.jsxs)(n.tr,{children:[(0,d.jsx)(n.th,{children:"Description"}),(0,d.jsx)(n.th,{children:"Class-name"})]})}),(0,d.jsxs)(n.tbody,{children:[(0,d.jsxs)(n.tr,{children:[(0,d.jsx)(n.td,{children:"Embeddings"}),(0,d.jsx)(n.td,{children:(0,d.jsx)(n.code,{children:"OpenAIEmbedding"})})]}),(0,d.jsxs)(n.tr,{children:[(0,d.jsx)(n.td,{children:"Chat models"}),(0,d.jsx)(n.td,{children:(0,d.jsx)(n.code,{children:"OpenAIChatCompletion"})})]}),(0,d.jsxs)(n.tr,{children:[(0,d.jsx)(n.td,{children:"Image generation models"}),(0,d.jsx)(n.td,{children:(0,d.jsx)(n.code,{children:"OpenAIImageCreation"})})]}),(0,d.jsxs)(n.tr,{children:[(0,d.jsx)(n.td,{children:"Image edit models"}),(0,d.jsx)(n.td,{children:(0,d.jsx)(n.code,{children:"OpenAIImageEdit"})})]}),(0,d.jsxs)(n.tr,{children:[(0,d.jsx)(n.td,{children:"Audio transcription models"}),(0,d.jsx)(n.td,{children:(0,d.jsx)(n.code,{children:"OpenAIAudioTranscription"})})]})]})]}),"\n",(0,d.jsx)(n.p,{children:(0,d.jsx)(n.strong,{children:"Usage"})}),"\n",(0,d.jsx)(n.pre,{children:(0,d.jsx)(n.code,{className:"language-python",children:"from superduperdb.ext.openai import OpenAI<ModelType> as ModelCls\n\ndb.add(Modelcls(identifier='my-model', **kwargs))\n"})}),"\n",(0,d.jsx)(n.h2,{id:"cohere",children:"Cohere"}),"\n",(0,d.jsx)(n.p,{children:(0,d.jsx)(n.strong,{children:"Supported"})}),"\n",(0,d.jsxs)(n.table,{children:[(0,d.jsx)(n.thead,{children:(0,d.jsxs)(n.tr,{children:[(0,d.jsx)(n.th,{children:"Description"}),(0,d.jsx)(n.th,{children:"Class-name"})]})}),(0,d.jsxs)(n.tbody,{children:[(0,d.jsxs)(n.tr,{children:[(0,d.jsx)(n.td,{children:"Embeddings"}),(0,d.jsx)(n.td,{children:(0,d.jsx)(n.code,{children:"CohereEmbedding"})})]}),(0,d.jsxs)(n.tr,{children:[(0,d.jsx)(n.td,{children:"Chat models"}),(0,d.jsx)(n.td,{children:(0,d.jsx)(n.code,{children:"CohereChatCompletion"})})]})]})]}),"\n",(0,d.jsx)(n.p,{children:(0,d.jsx)(n.strong,{children:"Usage"})}),"\n",(0,d.jsx)(n.pre,{children:(0,d.jsx)(n.code,{className:"language-python",children:"from superduperdb.ext.cohere import Cohere<ModelType> as ModelCls\n\ndb.add(Modelcls(identifier='my-model', **kwargs))\n"})}),"\n",(0,d.jsx)(n.h2,{id:"anthropic",children:"Anthropic"}),"\n",(0,d.jsx)(n.p,{children:(0,d.jsx)(n.strong,{children:"Supported"})}),"\n",(0,d.jsxs)(n.table,{children:[(0,d.jsx)(n.thead,{children:(0,d.jsxs)(n.tr,{children:[(0,d.jsx)(n.th,{children:"Description"}),(0,d.jsx)(n.th,{children:"Class-name"})]})}),(0,d.jsx)(n.tbody,{children:(0,d.jsxs)(n.tr,{children:[(0,d.jsx)(n.td,{children:"Chat models"}),(0,d.jsx)(n.td,{children:(0,d.jsx)(n.code,{children:"AnthropicCompletions"})})]})})]}),"\n",(0,d.jsx)(n.p,{children:(0,d.jsx)(n.strong,{children:"Usage"})}),"\n",(0,d.jsx)(n.pre,{children:(0,d.jsx)(n.code,{className:"language-python",children:"from superduperdb.ext.anthropic import Anthropic<ModelType> as ModelCls\n\ndb.add(Modelcls(identifier='my-model', **kwargs))\n"})}),"\n",(0,d.jsx)(n.h2,{id:"jina",children:"Jina"}),"\n",(0,d.jsx)(n.p,{children:(0,d.jsx)(n.strong,{children:"Supported"})}),"\n",(0,d.jsxs)(n.table,{children:[(0,d.jsx)(n.thead,{children:(0,d.jsxs)(n.tr,{children:[(0,d.jsx)(n.th,{children:"Description"}),(0,d.jsx)(n.th,{children:"Class-name"})]})}),(0,d.jsx)(n.tbody,{children:(0,d.jsxs)(n.tr,{children:[(0,d.jsx)(n.td,{children:"Embeddings"}),(0,d.jsx)(n.td,{children:(0,d.jsx)(n.code,{children:"JinaEmbedding"})})]})})]}),"\n",(0,d.jsx)(n.p,{children:(0,d.jsx)(n.strong,{children:"Usage"})}),"\n",(0,d.jsx)(n.pre,{children:(0,d.jsx)(n.code,{className:"language-python",children:"from superduperdb.ext.jina import JinaEmbedding\n\ndb.add(JinaEmbedding(identifier='jina-embeddings-v2-base-en', api_key='JINA_API_KEY')) # You can also set JINA_API_KEY as environment variable\n"})})]})}function h(e={}){const{wrapper:n}={...(0,r.a)(),...e.components};return n?(0,d.jsx)(n,{...e,children:(0,d.jsx)(a,{...e})}):a(e)}},11151:(e,n,s)=>{s.d(n,{Z:()=>o,a:()=>t});var d=s(67294);const r={},i=d.createContext(r);function t(e){const n=d.useContext(i);return d.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function o(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(r):e.components||r:t(e.components),d.createElement(i.Provider,{value:n},e.children)}}}]);