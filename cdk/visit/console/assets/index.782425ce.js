var q=Object.defineProperty;var E=Object.getOwnPropertySymbols;var O=Object.prototype.hasOwnProperty,_=Object.prototype.propertyIsEnumerable;var v=(t,n,i)=>n in t?q(t,n,{enumerable:!0,configurable:!0,writable:!0,value:i}):t[n]=i,u=(t,n)=>{for(var i in n||(n={}))O.call(n,i)&&v(t,i,n[i]);if(E)for(var i of E(n))_.call(n,i)&&v(t,i,n[i]);return t};import{j as F,C as k,S as L,c as R,a as p,b as C,d as x,r as f,u as I,L as y,o as B,e as N,f as w,g as H,R as z,h as g,i as U,k as J,B as V}from"./vendor.3b2ff3c3.js";const Y=function(){const n=document.createElement("link").relList;if(n&&n.supports&&n.supports("modulepreload"))return;for(const r of document.querySelectorAll('link[rel="modulepreload"]'))c(r);new MutationObserver(r=>{for(const a of r)if(a.type==="childList")for(const l of a.addedNodes)l.tagName==="LINK"&&l.rel==="modulepreload"&&c(l)}).observe(document,{childList:!0,subtree:!0});function i(r){const a={};return r.integrity&&(a.integrity=r.integrity),r.referrerpolicy&&(a.referrerPolicy=r.referrerpolicy),r.crossorigin==="use-credentials"?a.credentials="include":r.crossorigin==="anonymous"?a.credentials="omit":a.credentials="same-origin",a}function c(r){if(r.ep)return;r.ep=!0;const a=i(r);fetch(r.href,a)}};Y();const T="https://www.google.com",P=t=>t.toISOString().split("T")[0],G=[{slug:"cooper_library",name:"Cooper Library"},{slug:"watt_center",name:"Watt Family Innovation Center"},{slug:"cook_lab",name:"Cook Laboratory"}],K=["Male","Female","Other"],Q=["Accounting","Agribusiness","Agricultural Education","Agricultural Mechanization and Business","Agriculture","Animal and Veterinary Sciences","Anthropology","Applied Economics","Applied Health Research and Evaluation","Applied Psychology","Architecture","Art","Athletic Leadership","Automotive Engineering","Biochemistry","Biochemistry and Molecular Biology","Bioengineering","Biological Sciences","Biomedical Engineering","Biosystems Engineering","Business Administration","Chemical Engineering","Chemistry","City and Regional Planning","Civil Engineering","Communication","Communication, Technology and Society","Computer Engineering","Computer Information Systems","Computer Science","Construction Science and Management","Counselor Education","Criminal Justice","Curriculum and Instruction","Data Science and Analytics","Digital Production Arts","Early Childhood Education","Economics","Educational Leadership","Education Systems Improvement Science Ed.D.","Electrical Engineering","Elementary Education","Engineering and Science Education","English","Entomology","Environmental and Natural Resources","Environmental Engineering","Environmental Health Physics","Environmental Toxicology","Financial Management","Food, Nutrition and Culinary Sciences","Food, Nutrition and Packaging Sciences","Food Science and Human Nutrition","Food Technology","Forest Resource Management","Forest Resources","Genetics","Geology","Graphic Communications","Healthcare Genetics","Health Science","Historic Preservation","History","Horticulture","Human-Centered Computing","Human Capital Education and Development","Human Factors Psychology","Human Resource Development","Hydrogeology","Industrial Engineering","Industrial/Organizational Psychology","International Family and Community Studies","Landscape Architecture","Language and International Health","Language and International Business","Learning Sciences","Literacy","Literacy, Language and Culture","Management","Marketing","Materials Science and Engineering","Mathematical Sciences","Mathematics Teaching","Mechanical Engineering","Microbiology","Middle Level Education","Modern Languages","Nursing","Packaging Science","Pan African Studies","Parks, Recreation and Tourism Management","Philosophy","Photonic Science and Technology","Physics","Planning, Design and Built Environment","Plant and Environmental Sciences","Policy Studies","Political Science","Prepharmacy","Preprofessional Health Studies","Preveterinary Medicine","Performing Arts","Professional Communication","Psychology","Public Administration","Real Estate Development","Religious Studies","Resilient Urban Design","Rhetorics, Communication and Information Design","Science Teaching","Secondary Education","Sociology","Social Science","Special Education","Sports Communication","Student Affairs","Teacher Residency","Teaching and Learning","Transportation Safety Administration","Turfgrass","Wildlife and Fisheries Biology","Women's Leadership","World Cinema","Youth Development Leadership"],X=["Accounting","Adult/Extension Education","Aerospace Studies","Agricultural Business Management","Agricultural Mechanization and Business","American Sign Language Studies","Animal and Veterinary Sciences","Anthropology","Architecture","Art","Athletic Leadership","Biochemistry","Biological Sciences","British and Irish Studies","Brand Communications","Business Administration","Chemistry","Chinese Studies","Cluster","Communication Studies","Computer Science","Creative Writing","Crop and Soil Environmental Science","Cybersecurity","Digital Production Arts","East Asian Studies","Economics","English","Entomology","Entrepreneurship","Environmental Science and Policy","Equine Industry","Film Studies","Financial Management","Food Science","Forest Products","Forest Resource Management","French Studies","Gender, Sexuality and Women's Studies","Genetics","Geography","Geology","German Studies","Global Politics","Great Works","History","Horticulture","Human Resource Management","International Engineering and Science","Italian Studies","Japanese Studies","Legal Studies","Management","Management Information Systems","Mathematical Sciences","Microbiology","Middle Eastern Studies","Military Leadership","Music","Natural Resource Economics","Nonprofit Leadership","Nuclear Engineering and Radiological Sciences","Packaging Science","Pan African Studies","Park and Protected Area Management","Philosophy","Physics","Plant Pathology","Political and Legal Theory","Political Science","Precision Agriculture","Psychology","Public Policy","Race, Ethnicity and Migration","Religious Studies","Russian Area Studies","Science and Technology in Society","Screenwriting","Sociology","Spanish Studies","Spanish-American Area Studies","Sustainability","Theatre","Travel and Tourism","Turfgrass","Urban Forestry","Wildlife and Fisheries Biology","Women's Leadership","Writing","Youth Development Studies"],e=F.exports.jsx,s=F.exports.jsxs,Z=({control:t,name:n,values:i,id:c})=>{const r=i.map(a=>({label:a,value:a}));return e(k,{name:n,control:t,render:({field:{value:a,onChange:l,onBlur:d}})=>e(L,{id:c,className:"text-dark",options:r,value:r.filter(o=>o.value===a),onChange:o=>l(o.value),onBlur:d})})},A=({control:t,name:n,values:i,id:c})=>{const r=i.map(a=>({label:a,value:a}));return e(k,{name:n,control:t,render:({field:{value:a,onChange:l,onBlur:d}})=>e(L,{id:c,className:"text-dark",options:r,value:r.filter(o=>a==null?void 0:a.includes(o.value)),onChange:o=>l(o.map(h=>h.value)),onBlur:d,isMulti:!0,isSearchable:!0})})},ee=()=>s("div",{className:"text-muted w-full mt-5 fs-6 text-center",children:["This site is developed by students in Clemson's School of Computing Capstone.",e("br",{}),e("a",{className:"link-secondary text-muted",href:"https://github.com/clemsonMakerspace/unified-makerspace/tree/mainline/site/visitor-console",children:"Contribute to the code on GitHub"}),"."]}),m=({title:t,subtitle:n,children:i})=>s("div",{className:"container bg-primary p-5 rounded d-flex flex-column",style:{minHeight:"27rem",maxWidth:"50rem"},children:[s("div",{className:"mb-4 text-center",children:[e("h1",{className:"text-secondary fw-bold mb-1",children:t||"TITLE GOES HERE"}),!!n&&e("span",{className:"text-light fw-bold fs-4",children:n})]}),e("div",{className:"d-flex justify-content-center text-white",children:i}),e("div",{className:"flex-grow-1"}),e(ee,{})]}),ne=R({username:p().required(),firstname:p().required(),lastname:p().required(),gender:p().required(),birthday:C().required(),graddate:C().required(),major:x().required(),minor:x()}).required(),te=()=>{const[t,n]=f.exports.useState(!1),{register:i,handleSubmit:c,control:r,reset:a}=I({resolver:B(ne)}),l=c(o=>d(o)),d=o=>{const h={username:o.username,firstName:o.firstname,lastName:o.lastname,Gender:o.gender,DOB:P(o.birthday),Grad_Date:P(o.graddate),Major:o.major,Minor:o.minor};fetch(`${T}/register`,{method:"post",body:JSON.stringify(h)}).then(b=>{b.ok?(a(),n(!0)):alert("Registration unsuccessful")})};return t?e(m,{title:"Registration Successful"}):e(m,{title:"Makerspace Registration",subtitle:"Please Fill in Registration Information",children:e("div",{className:"d-flex flex-column align-items-center text-light",children:s("form",{className:"row",onSubmit:l,style:{maxWidth:"30rem"},children:[s("div",{className:"col-12 mb-2",children:[e("label",{htmlFor:"username",className:"form-label",children:"Username"}),e("input",u({id:"username",className:"form-control",type:"text",placeholder:"Enter username here"},i("username")))]}),s("div",{className:"col-md-6 mb-2",children:[e("label",{htmlFor:"firstname",className:"form-label",children:"Firstname"}),e("input",u({className:"form-control col-md-6",type:"text",id:"firstname",placeholder:"Firstname"},i("firstname")))]}),s("div",{className:"col-md-6 mb-2",children:[e("label",{htmlFor:"firstname",className:"form-label",children:"Lastname"}),e("input",u({className:"form-control",type:"text",id:"firstname",placeholder:"Lastname"},i("lastname")))]}),s("div",{className:"col-md-6",children:[e("label",{htmlFor:"gender",className:"form-label",children:"Gender"}),e(Z,{control:r,name:"gender",values:K})]}),s("div",{className:"col-md-6 mb-2",children:[e("label",{htmlFor:"birthday",className:"form-label",children:"Birthday"}),e("input",u({className:"form-control",type:"date",id:"birthday",placeholder:"birthday"},i("birthday")))]}),s("div",{className:"col-12 mb-2",children:[e("label",{htmlFor:"graddate",className:"form-label",children:"Expected Graduation Date"}),e("input",u({type:"date",className:"form-control",id:"graddate"},i("graddate")))]}),s("div",{className:"col-12 mb-2",children:[e("label",{htmlFor:"major",className:"form-label",children:"Major(s)"}),e(A,{id:"major",name:"major",control:r,values:Q})]}),s("div",{className:"col-12 mb-4",children:[e("label",{htmlFor:"minor",className:"form-label",children:"Minor(s)"}),e(A,{id:"minor",name:"minor",control:r,values:X})]}),s("div",{className:"d-flex justify-content-between",children:[e("button",{type:"submit",className:"btn btn-secondary mr-5",children:"Register"}),e(y,{to:"/",children:e("button",{className:"btn btn-link text-light",children:"Cancel"})})]})]})})})},ie=()=>e(m,{title:"Makerspace Sign-In",subtitle:"Location Selection",children:e("div",{className:"d-flex gap-3",children:G.map(({slug:t,name:n})=>e(y,{to:`/${t}`,children:e("button",{className:"btn btn-secondary",children:n})},t))})}),ae=()=>{const t=N();let[n]=w();const i=n.get("next")||"/",c=()=>e(m,{title:"Sign-In Sucessful",children:e(y,{to:i,className:"btn btn-secondary",children:"Continue"})});return e(H,{date:Date.now()+1e4,renderer:c,onComplete:()=>t(i)})},re=R({username:p().required()}).required(),M=({location:t,field_label:n,field_type:i,user_type:c,onCancel:r})=>{const a=N(),[l,d]=f.exports.useState(!1),{register:o,handleSubmit:h,formState:{errors:b}}=I({resolver:B(re)}),D=h(S=>j(S)),j=S=>{const $={username:S.username,location:t.name};d(!0),fetch(`${T}/visit`,{method:"post",body:JSON.stringify($)}).then(W=>{d(!1),W.ok?a(`/success?next=/${t.slug}`):a(`/error?next=/${t.slug}`)})};return l?e(m,{title:"Makerspace Sign-In",subtitle:"loading..."}):e(m,{title:"Makerspace Sign-In",subtitle:`as ${c}`,children:s("form",{onSubmit:D,children:[s("div",{className:"form-group mb-3",children:[e("label",{htmlFor:"username",className:"form-label",children:n}),e("input",u({id:"username",type:i,className:"form-control",placeholder:n},o("username"))),b.username&&s("span",{className:"form-text text-danger d-block",children:["Please enter your ",n.toLowerCase(),"."]})]}),s("div",{className:"d-flex justify-content-between",children:[e("button",{type:"submit",className:"btn btn-secondary mr-5",children:"Sign In"}),e("button",{className:"btn btn-link text-light",onClick:r,children:"Cancel"})]})]})})},se=({location:t})=>{const[n,i]=f.exports.useState(0),c=()=>i(0);return n===1?e(M,{user_type:"Clemson Student",field_label:"Username",field_type:"text",location:t,onCancel:c}):n===2?e(M,{user_type:"Guest Visitor",field_label:"Email",field_type:"email",location:t,onCancel:c}):e(m,{title:"Makerspace Sign-In",subtitle:`at ${t.name}`,children:s("div",{children:[e("button",{className:"btn-lg btn-secondary mb-3 d-block",style:{width:"250px"},onClick:()=>i(1),children:"Clemson User"}),e("button",{className:"btn-lg btn-accent d-block",style:{width:"250px"},onClick:()=>i(2),children:"Guest User"})]})})},oe=()=>{const t=N();let[n]=w();const i=n.get("next")||"/",c=()=>e(m,{title:"Sign-In Failed",subtitle:"there was a problem signing in",children:e(y,{to:i,className:"btn btn-secondary",children:"Continue"})});return e(H,{date:Date.now()+1e4,renderer:c,onComplete:()=>t(i)})},ce=()=>s("div",{children:[s("p",{style:{textAlign:"center",color:"white",paddingBottom:"100px"},children:[e("h1",{style:{fontSize:"350%"},children:"Error 404"}),e("h2",{children:"Page Not Found"})]}),e("p",{style:{textAlign:"center"},children:e(y,{to:"/",style:{color:"white",paddingBottom:"100px",fontSize:"200%"},children:"Go Back to Home Page"})})]}),le=()=>s(z,{children:[e(g,{path:"/",element:e(ie,{})}),e(g,{path:"/register",element:e(te,{})}),e(g,{path:"/success",element:e(ae,{})}),e(g,{path:"/error",element:e(oe,{})}),e(g,{path:"*",element:e(ce,{})}),G.map(t=>{const{slug:n}=t;return e(g,{path:`/${n}`,element:e(se,{location:t})},n)})]});var de="/assets/background.7cebd617.webp",me="/assets/makerspace_logo.21d32f19.webp";document.body.className="bg-dark";U.render(e(J.StrictMode,{children:s("div",{className:"pb-5",style:{backgroundImage:`url(${de})`,backgroundSize:"cover",minHeight:"100%"},children:[e("div",{className:"w-full pt-4 ps-4 pb-5",children:e("img",{src:me,style:{maxWidth:"100%"},alt:"Clemson Makerspace Logo"})}),e(V,{children:e(le,{})})]})}),document.getElementById("root"));