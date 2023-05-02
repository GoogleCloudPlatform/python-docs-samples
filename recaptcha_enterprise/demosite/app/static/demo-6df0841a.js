// Copyright 2023 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


/******************************************************************************
Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
***************************************************************************** */
/* global Reflect, Promise */

var extendStatics = function(d, b) {
    extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
    return extendStatics(d, b);
};

function __extends(d, b) {
    if (typeof b !== "function" && b !== null)
        throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
    extendStatics(d, b);
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
}

var __assign = function() {
    __assign = Object.assign || function __assign(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p)) t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};

function __decorate(decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
}

function __values(o) {
    var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
    if (m) return m.call(o);
    if (o && typeof o.length === "number") return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
    throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
}

/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const e$7=e=>n=>"function"==typeof n?((e,n)=>(customElements.define(e,n),n))(e,n):((e,n)=>{const{kind:t,elements:s}=n;return {kind:t,elements:s,finisher(n){customElements.define(e,n);}}})(e,n);

/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const i$5=(i,e)=>"method"===e.kind&&e.descriptor&&!("value"in e.descriptor)?{...e,finisher(n){n.createProperty(e.key,i);}}:{kind:"field",key:Symbol(),placement:"own",descriptor:{},originalKey:e.key,initializer(){"function"==typeof e.initializer&&(this[e.key]=e.initializer.call(this));},finisher(n){n.createProperty(e.key,i);}};function e$6(e){return (n,t)=>void 0!==t?((i,e,n)=>{e.constructor.createProperty(n,i);})(e,n,t):i$5(e,n)}

/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */function t$3(t){return e$6({...t,state:!0})}

/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const o$5=({finisher:e,descriptor:t})=>(o,n)=>{var r;if(void 0===n){const n=null!==(r=o.originalKey)&&void 0!==r?r:o.key,i=null!=t?{kind:"method",placement:"prototype",key:n,descriptor:t(o.key)}:{...o,key:n};return null!=e&&(i.finisher=function(t){e(t,n);}),i}{const r=o.constructor;void 0!==t&&Object.defineProperty(o,n,t(n)),null==e||e(r,n);}};

/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */function e$5(e){return o$5({finisher:(r,t)=>{Object.assign(r.prototype[t],e);}})}

/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */function i$4(i,n){return o$5({descriptor:o=>{const t={get(){var o,n;return null!==(n=null===(o=this.renderRoot)||void 0===o?void 0:o.querySelector(i))&&void 0!==n?n:null},enumerable:!0,configurable:!0};if(n){const n="symbol"==typeof o?Symbol():"__"+o;t.get=function(){var o,t;return void 0===this[n]&&(this[n]=null!==(t=null===(o=this.renderRoot)||void 0===o?void 0:o.querySelector(i))&&void 0!==t?t:null),this[n]};}return t}})}

/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
function e$4(e){return o$5({descriptor:r=>({async get(){var r;return await this.updateComplete,null===(r=this.renderRoot)||void 0===r?void 0:r.querySelector(e)},enumerable:!0,configurable:!0})})}

/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */var n$4;null!=(null===(n$4=window.HTMLSlotElement)||void 0===n$4?void 0:n$4.prototype.assignedElements)?(o,n)=>o.assignedElements(n):(o,n)=>o.assignedNodes(n).filter((o=>o.nodeType===Node.ELEMENT_NODE));

/**
 * @license
 * Copyright 2018 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
function matches(element, selector) {
    var nativeMatches = element.matches
        || element.webkitMatchesSelector
        || element.msMatchesSelector;
    return nativeMatches.call(element, selector);
}

/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const t$2=window,e$3=t$2.ShadowRoot&&(void 0===t$2.ShadyCSS||t$2.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,s$3=Symbol(),n$3=new WeakMap;let o$4 = class o{constructor(t,e,n){if(this._$cssResult$=!0,n!==s$3)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e;}get styleSheet(){let t=this.o;const s=this.t;if(e$3&&void 0===t){const e=void 0!==s&&1===s.length;e&&(t=n$3.get(s)),void 0===t&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),e&&n$3.set(s,t));}return t}toString(){return this.cssText}};const r$2=t=>new o$4("string"==typeof t?t:t+"",void 0,s$3),i$3=(t,...e)=>{const n=1===t.length?t[0]:e.reduce(((e,s,n)=>e+(t=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(s)+t[n+1]),t[0]);return new o$4(n,t,s$3)},S$1=(s,n)=>{e$3?s.adoptedStyleSheets=n.map((t=>t instanceof CSSStyleSheet?t:t.styleSheet)):n.forEach((e=>{const n=document.createElement("style"),o=t$2.litNonce;void 0!==o&&n.setAttribute("nonce",o),n.textContent=e.cssText,s.appendChild(n);}));},c$1=e$3?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const s of t.cssRules)e+=s.cssText;return r$2(e)})(t):t;

/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */var s$2;const e$2=window,r$1=e$2.trustedTypes,h$1=r$1?r$1.emptyScript:"",o$3=e$2.reactiveElementPolyfillSupport,n$2={toAttribute(t,i){switch(i){case Boolean:t=t?h$1:null;break;case Object:case Array:t=null==t?t:JSON.stringify(t);}return t},fromAttribute(t,i){let s=t;switch(i){case Boolean:s=null!==t;break;case Number:s=null===t?null:Number(t);break;case Object:case Array:try{s=JSON.parse(t);}catch(t){s=null;}}return s}},a$1=(t,i)=>i!==t&&(i==i||t==t),l$3={attribute:!0,type:String,converter:n$2,reflect:!1,hasChanged:a$1};let d$1 = class d extends HTMLElement{constructor(){super(),this._$Ei=new Map,this.isUpdatePending=!1,this.hasUpdated=!1,this._$El=null,this.u();}static addInitializer(t){var i;this.finalize(),(null!==(i=this.h)&&void 0!==i?i:this.h=[]).push(t);}static get observedAttributes(){this.finalize();const t=[];return this.elementProperties.forEach(((i,s)=>{const e=this._$Ep(s,i);void 0!==e&&(this._$Ev.set(e,s),t.push(e));})),t}static createProperty(t,i=l$3){if(i.state&&(i.attribute=!1),this.finalize(),this.elementProperties.set(t,i),!i.noAccessor&&!this.prototype.hasOwnProperty(t)){const s="symbol"==typeof t?Symbol():"__"+t,e=this.getPropertyDescriptor(t,s,i);void 0!==e&&Object.defineProperty(this.prototype,t,e);}}static getPropertyDescriptor(t,i,s){return {get(){return this[i]},set(e){const r=this[t];this[i]=e,this.requestUpdate(t,r,s);},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)||l$3}static finalize(){if(this.hasOwnProperty("finalized"))return !1;this.finalized=!0;const t=Object.getPrototypeOf(this);if(t.finalize(),void 0!==t.h&&(this.h=[...t.h]),this.elementProperties=new Map(t.elementProperties),this._$Ev=new Map,this.hasOwnProperty("properties")){const t=this.properties,i=[...Object.getOwnPropertyNames(t),...Object.getOwnPropertySymbols(t)];for(const s of i)this.createProperty(s,t[s]);}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(i){const s=[];if(Array.isArray(i)){const e=new Set(i.flat(1/0).reverse());for(const i of e)s.unshift(c$1(i));}else void 0!==i&&s.push(c$1(i));return s}static _$Ep(t,i){const s=i.attribute;return !1===s?void 0:"string"==typeof s?s:"string"==typeof t?t.toLowerCase():void 0}u(){var t;this._$E_=new Promise((t=>this.enableUpdating=t)),this._$AL=new Map,this._$Eg(),this.requestUpdate(),null===(t=this.constructor.h)||void 0===t||t.forEach((t=>t(this)));}addController(t){var i,s;(null!==(i=this._$ES)&&void 0!==i?i:this._$ES=[]).push(t),void 0!==this.renderRoot&&this.isConnected&&(null===(s=t.hostConnected)||void 0===s||s.call(t));}removeController(t){var i;null===(i=this._$ES)||void 0===i||i.splice(this._$ES.indexOf(t)>>>0,1);}_$Eg(){this.constructor.elementProperties.forEach(((t,i)=>{this.hasOwnProperty(i)&&(this._$Ei.set(i,this[i]),delete this[i]);}));}createRenderRoot(){var t;const s=null!==(t=this.shadowRoot)&&void 0!==t?t:this.attachShadow(this.constructor.shadowRootOptions);return S$1(s,this.constructor.elementStyles),s}connectedCallback(){var t;void 0===this.renderRoot&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),null===(t=this._$ES)||void 0===t||t.forEach((t=>{var i;return null===(i=t.hostConnected)||void 0===i?void 0:i.call(t)}));}enableUpdating(t){}disconnectedCallback(){var t;null===(t=this._$ES)||void 0===t||t.forEach((t=>{var i;return null===(i=t.hostDisconnected)||void 0===i?void 0:i.call(t)}));}attributeChangedCallback(t,i,s){this._$AK(t,s);}_$EO(t,i,s=l$3){var e;const r=this.constructor._$Ep(t,s);if(void 0!==r&&!0===s.reflect){const h=(void 0!==(null===(e=s.converter)||void 0===e?void 0:e.toAttribute)?s.converter:n$2).toAttribute(i,s.type);this._$El=t,null==h?this.removeAttribute(r):this.setAttribute(r,h),this._$El=null;}}_$AK(t,i){var s;const e=this.constructor,r=e._$Ev.get(t);if(void 0!==r&&this._$El!==r){const t=e.getPropertyOptions(r),h="function"==typeof t.converter?{fromAttribute:t.converter}:void 0!==(null===(s=t.converter)||void 0===s?void 0:s.fromAttribute)?t.converter:n$2;this._$El=r,this[r]=h.fromAttribute(i,t.type),this._$El=null;}}requestUpdate(t,i,s){let e=!0;void 0!==t&&(((s=s||this.constructor.getPropertyOptions(t)).hasChanged||a$1)(this[t],i)?(this._$AL.has(t)||this._$AL.set(t,i),!0===s.reflect&&this._$El!==t&&(void 0===this._$EC&&(this._$EC=new Map),this._$EC.set(t,s))):e=!1),!this.isUpdatePending&&e&&(this._$E_=this._$Ej());}async _$Ej(){this.isUpdatePending=!0;try{await this._$E_;}catch(t){Promise.reject(t);}const t=this.scheduleUpdate();return null!=t&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){var t;if(!this.isUpdatePending)return;this.hasUpdated,this._$Ei&&(this._$Ei.forEach(((t,i)=>this[i]=t)),this._$Ei=void 0);let i=!1;const s=this._$AL;try{i=this.shouldUpdate(s),i?(this.willUpdate(s),null===(t=this._$ES)||void 0===t||t.forEach((t=>{var i;return null===(i=t.hostUpdate)||void 0===i?void 0:i.call(t)})),this.update(s)):this._$Ek();}catch(t){throw i=!1,this._$Ek(),t}i&&this._$AE(s);}willUpdate(t){}_$AE(t){var i;null===(i=this._$ES)||void 0===i||i.forEach((t=>{var i;return null===(i=t.hostUpdated)||void 0===i?void 0:i.call(t)})),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t);}_$Ek(){this._$AL=new Map,this.isUpdatePending=!1;}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$E_}shouldUpdate(t){return !0}update(t){void 0!==this._$EC&&(this._$EC.forEach(((t,i)=>this._$EO(i,this[i],t))),this._$EC=void 0),this._$Ek();}updated(t){}firstUpdated(t){}};d$1.finalized=!0,d$1.elementProperties=new Map,d$1.elementStyles=[],d$1.shadowRootOptions={mode:"open"},null==o$3||o$3({ReactiveElement:d$1}),(null!==(s$2=e$2.reactiveElementVersions)&&void 0!==s$2?s$2:e$2.reactiveElementVersions=[]).push("1.6.1");

/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var t$1;const i$2=window,s$1=i$2.trustedTypes,e$1=s$1?s$1.createPolicy("lit-html",{createHTML:t=>t}):void 0,o$2="$lit$",n$1=`lit$${(Math.random()+"").slice(9)}$`,l$2="?"+n$1,h=`<${l$2}>`,r=document,d=()=>r.createComment(""),u=t=>null===t||"object"!=typeof t&&"function"!=typeof t,c=Array.isArray,v=t=>c(t)||"function"==typeof(null==t?void 0:t[Symbol.iterator]),a="[ \t\n\f\r]",f=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,_=/-->/g,m=/>/g,p=RegExp(`>|${a}(?:([^\\s"'>=/]+)(${a}*=${a}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),g=/'/g,$=/"/g,y=/^(?:script|style|textarea|title)$/i,w=t=>(i,...s)=>({_$litType$:t,strings:i,values:s}),x=w(1),T=Symbol.for("lit-noChange"),A=Symbol.for("lit-nothing"),E=new WeakMap,C=r.createTreeWalker(r,129,null,!1),P=(t,i)=>{const s=t.length-1,l=[];let r,d=2===i?"<svg>":"",u=f;for(let i=0;i<s;i++){const s=t[i];let e,c,v=-1,a=0;for(;a<s.length&&(u.lastIndex=a,c=u.exec(s),null!==c);)a=u.lastIndex,u===f?"!--"===c[1]?u=_:void 0!==c[1]?u=m:void 0!==c[2]?(y.test(c[2])&&(r=RegExp("</"+c[2],"g")),u=p):void 0!==c[3]&&(u=p):u===p?">"===c[0]?(u=null!=r?r:f,v=-1):void 0===c[1]?v=-2:(v=u.lastIndex-c[2].length,e=c[1],u=void 0===c[3]?p:'"'===c[3]?$:g):u===$||u===g?u=p:u===_||u===m?u=f:(u=p,r=void 0);const w=u===p&&t[i+1].startsWith("/>")?" ":"";d+=u===f?s+h:v>=0?(l.push(e),s.slice(0,v)+o$2+s.slice(v)+n$1+w):s+n$1+(-2===v?(l.push(void 0),i):w);}const c=d+(t[s]||"<?>")+(2===i?"</svg>":"");if(!Array.isArray(t)||!t.hasOwnProperty("raw"))throw Error("invalid template strings array");return [void 0!==e$1?e$1.createHTML(c):c,l]};class V{constructor({strings:t,_$litType$:i},e){let h;this.parts=[];let r=0,u=0;const c=t.length-1,v=this.parts,[a,f]=P(t,i);if(this.el=V.createElement(a,e),C.currentNode=this.el.content,2===i){const t=this.el.content,i=t.firstChild;i.remove(),t.append(...i.childNodes);}for(;null!==(h=C.nextNode())&&v.length<c;){if(1===h.nodeType){if(h.hasAttributes()){const t=[];for(const i of h.getAttributeNames())if(i.endsWith(o$2)||i.startsWith(n$1)){const s=f[u++];if(t.push(i),void 0!==s){const t=h.getAttribute(s.toLowerCase()+o$2).split(n$1),i=/([.?@])?(.*)/.exec(s);v.push({type:1,index:r,name:i[2],strings:t,ctor:"."===i[1]?k:"?"===i[1]?I:"@"===i[1]?L:R});}else v.push({type:6,index:r});}for(const i of t)h.removeAttribute(i);}if(y.test(h.tagName)){const t=h.textContent.split(n$1),i=t.length-1;if(i>0){h.textContent=s$1?s$1.emptyScript:"";for(let s=0;s<i;s++)h.append(t[s],d()),C.nextNode(),v.push({type:2,index:++r});h.append(t[i],d());}}}else if(8===h.nodeType)if(h.data===l$2)v.push({type:2,index:r});else {let t=-1;for(;-1!==(t=h.data.indexOf(n$1,t+1));)v.push({type:7,index:r}),t+=n$1.length-1;}r++;}}static createElement(t,i){const s=r.createElement("template");return s.innerHTML=t,s}}function N(t,i,s=t,e){var o,n,l,h;if(i===T)return i;let r=void 0!==e?null===(o=s._$Co)||void 0===o?void 0:o[e]:s._$Cl;const d=u(i)?void 0:i._$litDirective$;return (null==r?void 0:r.constructor)!==d&&(null===(n=null==r?void 0:r._$AO)||void 0===n||n.call(r,!1),void 0===d?r=void 0:(r=new d(t),r._$AT(t,s,e)),void 0!==e?(null!==(l=(h=s)._$Co)&&void 0!==l?l:h._$Co=[])[e]=r:s._$Cl=r),void 0!==r&&(i=N(t,r._$AS(t,i.values),r,e)),i}class S{constructor(t,i){this.u=[],this._$AN=void 0,this._$AD=t,this._$AM=i;}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}v(t){var i;const{el:{content:s},parts:e}=this._$AD,o=(null!==(i=null==t?void 0:t.creationScope)&&void 0!==i?i:r).importNode(s,!0);C.currentNode=o;let n=C.nextNode(),l=0,h=0,d=e[0];for(;void 0!==d;){if(l===d.index){let i;2===d.type?i=new M(n,n.nextSibling,this,t):1===d.type?i=new d.ctor(n,d.name,d.strings,this,t):6===d.type&&(i=new z(n,this,t)),this.u.push(i),d=e[++h];}l!==(null==d?void 0:d.index)&&(n=C.nextNode(),l++);}return o}p(t){let i=0;for(const s of this.u)void 0!==s&&(void 0!==s.strings?(s._$AI(t,s,i),i+=s.strings.length-2):s._$AI(t[i])),i++;}}class M{constructor(t,i,s,e){var o;this.type=2,this._$AH=A,this._$AN=void 0,this._$AA=t,this._$AB=i,this._$AM=s,this.options=e,this._$Cm=null===(o=null==e?void 0:e.isConnected)||void 0===o||o;}get _$AU(){var t,i;return null!==(i=null===(t=this._$AM)||void 0===t?void 0:t._$AU)&&void 0!==i?i:this._$Cm}get parentNode(){let t=this._$AA.parentNode;const i=this._$AM;return void 0!==i&&11===(null==t?void 0:t.nodeType)&&(t=i.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,i=this){t=N(this,t,i),u(t)?t===A||null==t||""===t?(this._$AH!==A&&this._$AR(),this._$AH=A):t!==this._$AH&&t!==T&&this.g(t):void 0!==t._$litType$?this.$(t):void 0!==t.nodeType?this.T(t):v(t)?this.k(t):this.g(t);}S(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.S(t));}g(t){this._$AH!==A&&u(this._$AH)?this._$AA.nextSibling.data=t:this.T(r.createTextNode(t)),this._$AH=t;}$(t){var i;const{values:s,_$litType$:e}=t,o="number"==typeof e?this._$AC(t):(void 0===e.el&&(e.el=V.createElement(e.h,this.options)),e);if((null===(i=this._$AH)||void 0===i?void 0:i._$AD)===o)this._$AH.p(s);else {const t=new S(o,this),i=t.v(this.options);t.p(s),this.T(i),this._$AH=t;}}_$AC(t){let i=E.get(t.strings);return void 0===i&&E.set(t.strings,i=new V(t)),i}k(t){c(this._$AH)||(this._$AH=[],this._$AR());const i=this._$AH;let s,e=0;for(const o of t)e===i.length?i.push(s=new M(this.S(d()),this.S(d()),this,this.options)):s=i[e],s._$AI(o),e++;e<i.length&&(this._$AR(s&&s._$AB.nextSibling,e),i.length=e);}_$AR(t=this._$AA.nextSibling,i){var s;for(null===(s=this._$AP)||void 0===s||s.call(this,!1,!0,i);t&&t!==this._$AB;){const i=t.nextSibling;t.remove(),t=i;}}setConnected(t){var i;void 0===this._$AM&&(this._$Cm=t,null===(i=this._$AP)||void 0===i||i.call(this,t));}}class R{constructor(t,i,s,e,o){this.type=1,this._$AH=A,this._$AN=void 0,this.element=t,this.name=i,this._$AM=e,this.options=o,s.length>2||""!==s[0]||""!==s[1]?(this._$AH=Array(s.length-1).fill(new String),this.strings=s):this._$AH=A;}get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}_$AI(t,i=this,s,e){const o=this.strings;let n=!1;if(void 0===o)t=N(this,t,i,0),n=!u(t)||t!==this._$AH&&t!==T,n&&(this._$AH=t);else {const e=t;let l,h;for(t=o[0],l=0;l<o.length-1;l++)h=N(this,e[s+l],i,l),h===T&&(h=this._$AH[l]),n||(n=!u(h)||h!==this._$AH[l]),h===A?t=A:t!==A&&(t+=(null!=h?h:"")+o[l+1]),this._$AH[l]=h;}n&&!e&&this.j(t);}j(t){t===A?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,null!=t?t:"");}}class k extends R{constructor(){super(...arguments),this.type=3;}j(t){this.element[this.name]=t===A?void 0:t;}}const H=s$1?s$1.emptyScript:"";class I extends R{constructor(){super(...arguments),this.type=4;}j(t){t&&t!==A?this.element.setAttribute(this.name,H):this.element.removeAttribute(this.name);}}class L extends R{constructor(t,i,s,e,o){super(t,i,s,e,o),this.type=5;}_$AI(t,i=this){var s;if((t=null!==(s=N(this,t,i,0))&&void 0!==s?s:A)===T)return;const e=this._$AH,o=t===A&&e!==A||t.capture!==e.capture||t.once!==e.once||t.passive!==e.passive,n=t!==A&&(e===A||o);o&&this.element.removeEventListener(this.name,this,e),n&&this.element.addEventListener(this.name,this,t),this._$AH=t;}handleEvent(t){var i,s;"function"==typeof this._$AH?this._$AH.call(null!==(s=null===(i=this.options)||void 0===i?void 0:i.host)&&void 0!==s?s:this.element,t):this._$AH.handleEvent(t);}}class z{constructor(t,i,s){this.element=t,this.type=6,this._$AN=void 0,this._$AM=i,this.options=s;}get _$AU(){return this._$AM._$AU}_$AI(t){N(this,t);}}const j=i$2.litHtmlPolyfillSupport;null==j||j(V,M),(null!==(t$1=i$2.litHtmlVersions)&&void 0!==t$1?t$1:i$2.litHtmlVersions=[]).push("2.7.0");const B=(t,i,s)=>{var e,o;const n=null!==(e=null==s?void 0:s.renderBefore)&&void 0!==e?e:i;let l=n._$litPart$;if(void 0===l){const t=null!==(o=null==s?void 0:s.renderBefore)&&void 0!==o?o:null;n._$litPart$=l=new M(i.insertBefore(d(),t),t,void 0,null!=s?s:{});}return l._$AI(t),l};

/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */var l$1,o$1;class s extends d$1{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0;}createRenderRoot(){var t,e;const i=super.createRenderRoot();return null!==(t=(e=this.renderOptions).renderBefore)&&void 0!==t||(e.renderBefore=i.firstChild),i}update(t){const i=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=B(i,this.renderRoot,this.renderOptions);}connectedCallback(){var t;super.connectedCallback(),null===(t=this._$Do)||void 0===t||t.setConnected(!0);}disconnectedCallback(){var t;super.disconnectedCallback(),null===(t=this._$Do)||void 0===t||t.setConnected(!1);}render(){return T}}s.finalized=!0,s._$litElement$=!0,null===(l$1=globalThis.litElementHydrateSupport)||void 0===l$1||l$1.call(globalThis,{LitElement:s});const n=globalThis.litElementPolyfillSupport;null==n||n({LitElement:s});(null!==(o$1=globalThis.litElementVersions)&&void 0!==o$1?o$1:globalThis.litElementVersions=[]).push("3.3.0");

/**
 * @license
 * Copyright 2018 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
const fn = () => { };
const optionsBlock = {
    get passive() {
        return false;
    }
};
document.addEventListener('x', fn, optionsBlock);
document.removeEventListener('x', fn);

/**
 * @license
 * Copyright 2018 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
/** @soyCompatible */
class BaseElement extends s {
    click() {
        if (this.mdcRoot) {
            this.mdcRoot.focus();
            this.mdcRoot.click();
            return;
        }
        super.click();
    }
    /**
     * Create and attach the MDC Foundation to the instance
     */
    createFoundation() {
        if (this.mdcFoundation !== undefined) {
            this.mdcFoundation.destroy();
        }
        if (this.mdcFoundationClass) {
            this.mdcFoundation = new this.mdcFoundationClass(this.createAdapter());
            this.mdcFoundation.init();
        }
    }
    firstUpdated() {
        this.createFoundation();
    }
}

/**
 * @license
 * Copyright 2016 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var MDCFoundation = /** @class */ (function () {
    function MDCFoundation(adapter) {
        if (adapter === void 0) { adapter = {}; }
        this.adapter = adapter;
    }
    Object.defineProperty(MDCFoundation, "cssClasses", {
        get: function () {
            // Classes extending MDCFoundation should implement this method to return an object which exports every
            // CSS class the foundation class needs as a property. e.g. {ACTIVE: 'mdc-component--active'}
            return {};
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(MDCFoundation, "strings", {
        get: function () {
            // Classes extending MDCFoundation should implement this method to return an object which exports all
            // semantic strings as constants. e.g. {ARIA_ROLE: 'tablist'}
            return {};
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(MDCFoundation, "numbers", {
        get: function () {
            // Classes extending MDCFoundation should implement this method to return an object which exports all
            // of its semantic numbers as constants. e.g. {ANIMATION_DELAY_MS: 350}
            return {};
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(MDCFoundation, "defaultAdapter", {
        get: function () {
            // Classes extending MDCFoundation may choose to implement this getter in order to provide a convenient
            // way of viewing the necessary methods of an adapter. In the future, this could also be used for adapter
            // validation.
            return {};
        },
        enumerable: false,
        configurable: true
    });
    MDCFoundation.prototype.init = function () {
        // Subclasses should override this method to perform initialization routines (registering events, etc.)
    };
    MDCFoundation.prototype.destroy = function () {
        // Subclasses should override this method to perform de-initialization routines (de-registering events, etc.)
    };
    return MDCFoundation;
}());

/**
 * @license
 * Copyright 2016 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var cssClasses = {
    // Ripple is a special case where the "root" component is really a "mixin" of sorts,
    // given that it's an 'upgrade' to an existing component. That being said it is the root
    // CSS class that all other CSS classes derive from.
    BG_FOCUSED: 'mdc-ripple-upgraded--background-focused',
    FG_ACTIVATION: 'mdc-ripple-upgraded--foreground-activation',
    FG_DEACTIVATION: 'mdc-ripple-upgraded--foreground-deactivation',
    ROOT: 'mdc-ripple-upgraded',
    UNBOUNDED: 'mdc-ripple-upgraded--unbounded',
};
var strings = {
    VAR_FG_SCALE: '--mdc-ripple-fg-scale',
    VAR_FG_SIZE: '--mdc-ripple-fg-size',
    VAR_FG_TRANSLATE_END: '--mdc-ripple-fg-translate-end',
    VAR_FG_TRANSLATE_START: '--mdc-ripple-fg-translate-start',
    VAR_LEFT: '--mdc-ripple-left',
    VAR_TOP: '--mdc-ripple-top',
};
var numbers = {
    DEACTIVATION_TIMEOUT_MS: 225,
    FG_DEACTIVATION_MS: 150,
    INITIAL_ORIGIN_SCALE: 0.6,
    PADDING: 10,
    TAP_DELAY_MS: 300, // Delay between touch and simulated mouse events on touch devices
};

/**
 * Stores result from supportsCssVariables to avoid redundant processing to
 * detect CSS custom variable support.
 */
function getNormalizedEventCoords(evt, pageOffset, clientRect) {
    if (!evt) {
        return { x: 0, y: 0 };
    }
    var x = pageOffset.x, y = pageOffset.y;
    var documentX = x + clientRect.left;
    var documentY = y + clientRect.top;
    var normalizedX;
    var normalizedY;
    // Determine touch point relative to the ripple container.
    if (evt.type === 'touchstart') {
        var touchEvent = evt;
        normalizedX = touchEvent.changedTouches[0].pageX - documentX;
        normalizedY = touchEvent.changedTouches[0].pageY - documentY;
    }
    else {
        var mouseEvent = evt;
        normalizedX = mouseEvent.pageX - documentX;
        normalizedY = mouseEvent.pageY - documentY;
    }
    return { x: normalizedX, y: normalizedY };
}

/**
 * @license
 * Copyright 2016 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
// Activation events registered on the root element of each instance for activation
var ACTIVATION_EVENT_TYPES = [
    'touchstart', 'pointerdown', 'mousedown', 'keydown',
];
// Deactivation events registered on documentElement when a pointer-related down event occurs
var POINTER_DEACTIVATION_EVENT_TYPES = [
    'touchend', 'pointerup', 'mouseup', 'contextmenu',
];
// simultaneous nested activations
var activatedTargets = [];
var MDCRippleFoundation = /** @class */ (function (_super) {
    __extends(MDCRippleFoundation, _super);
    function MDCRippleFoundation(adapter) {
        var _this = _super.call(this, __assign(__assign({}, MDCRippleFoundation.defaultAdapter), adapter)) || this;
        _this.activationAnimationHasEnded = false;
        _this.activationTimer = 0;
        _this.fgDeactivationRemovalTimer = 0;
        _this.fgScale = '0';
        _this.frame = { width: 0, height: 0 };
        _this.initialSize = 0;
        _this.layoutFrame = 0;
        _this.maxRadius = 0;
        _this.unboundedCoords = { left: 0, top: 0 };
        _this.activationState = _this.defaultActivationState();
        _this.activationTimerCallback = function () {
            _this.activationAnimationHasEnded = true;
            _this.runDeactivationUXLogicIfReady();
        };
        _this.activateHandler = function (e) {
            _this.activateImpl(e);
        };
        _this.deactivateHandler = function () {
            _this.deactivateImpl();
        };
        _this.focusHandler = function () {
            _this.handleFocus();
        };
        _this.blurHandler = function () {
            _this.handleBlur();
        };
        _this.resizeHandler = function () {
            _this.layout();
        };
        return _this;
    }
    Object.defineProperty(MDCRippleFoundation, "cssClasses", {
        get: function () {
            return cssClasses;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(MDCRippleFoundation, "strings", {
        get: function () {
            return strings;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(MDCRippleFoundation, "numbers", {
        get: function () {
            return numbers;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(MDCRippleFoundation, "defaultAdapter", {
        get: function () {
            return {
                addClass: function () { return undefined; },
                browserSupportsCssVars: function () { return true; },
                computeBoundingRect: function () {
                    return ({ top: 0, right: 0, bottom: 0, left: 0, width: 0, height: 0 });
                },
                containsEventTarget: function () { return true; },
                deregisterDocumentInteractionHandler: function () { return undefined; },
                deregisterInteractionHandler: function () { return undefined; },
                deregisterResizeHandler: function () { return undefined; },
                getWindowPageOffset: function () { return ({ x: 0, y: 0 }); },
                isSurfaceActive: function () { return true; },
                isSurfaceDisabled: function () { return true; },
                isUnbounded: function () { return true; },
                registerDocumentInteractionHandler: function () { return undefined; },
                registerInteractionHandler: function () { return undefined; },
                registerResizeHandler: function () { return undefined; },
                removeClass: function () { return undefined; },
                updateCssVariable: function () { return undefined; },
            };
        },
        enumerable: false,
        configurable: true
    });
    MDCRippleFoundation.prototype.init = function () {
        var _this = this;
        var supportsPressRipple = this.supportsPressRipple();
        this.registerRootHandlers(supportsPressRipple);
        if (supportsPressRipple) {
            var _a = MDCRippleFoundation.cssClasses, ROOT_1 = _a.ROOT, UNBOUNDED_1 = _a.UNBOUNDED;
            requestAnimationFrame(function () {
                _this.adapter.addClass(ROOT_1);
                if (_this.adapter.isUnbounded()) {
                    _this.adapter.addClass(UNBOUNDED_1);
                    // Unbounded ripples need layout logic applied immediately to set coordinates for both shade and ripple
                    _this.layoutInternal();
                }
            });
        }
    };
    MDCRippleFoundation.prototype.destroy = function () {
        var _this = this;
        if (this.supportsPressRipple()) {
            if (this.activationTimer) {
                clearTimeout(this.activationTimer);
                this.activationTimer = 0;
                this.adapter.removeClass(MDCRippleFoundation.cssClasses.FG_ACTIVATION);
            }
            if (this.fgDeactivationRemovalTimer) {
                clearTimeout(this.fgDeactivationRemovalTimer);
                this.fgDeactivationRemovalTimer = 0;
                this.adapter.removeClass(MDCRippleFoundation.cssClasses.FG_DEACTIVATION);
            }
            var _a = MDCRippleFoundation.cssClasses, ROOT_2 = _a.ROOT, UNBOUNDED_2 = _a.UNBOUNDED;
            requestAnimationFrame(function () {
                _this.adapter.removeClass(ROOT_2);
                _this.adapter.removeClass(UNBOUNDED_2);
                _this.removeCssVars();
            });
        }
        this.deregisterRootHandlers();
        this.deregisterDeactivationHandlers();
    };
    /**
     * @param evt Optional event containing position information.
     */
    MDCRippleFoundation.prototype.activate = function (evt) {
        this.activateImpl(evt);
    };
    MDCRippleFoundation.prototype.deactivate = function () {
        this.deactivateImpl();
    };
    MDCRippleFoundation.prototype.layout = function () {
        var _this = this;
        if (this.layoutFrame) {
            cancelAnimationFrame(this.layoutFrame);
        }
        this.layoutFrame = requestAnimationFrame(function () {
            _this.layoutInternal();
            _this.layoutFrame = 0;
        });
    };
    MDCRippleFoundation.prototype.setUnbounded = function (unbounded) {
        var UNBOUNDED = MDCRippleFoundation.cssClasses.UNBOUNDED;
        if (unbounded) {
            this.adapter.addClass(UNBOUNDED);
        }
        else {
            this.adapter.removeClass(UNBOUNDED);
        }
    };
    MDCRippleFoundation.prototype.handleFocus = function () {
        var _this = this;
        requestAnimationFrame(function () { return _this.adapter.addClass(MDCRippleFoundation.cssClasses.BG_FOCUSED); });
    };
    MDCRippleFoundation.prototype.handleBlur = function () {
        var _this = this;
        requestAnimationFrame(function () { return _this.adapter.removeClass(MDCRippleFoundation.cssClasses.BG_FOCUSED); });
    };
    /**
     * We compute this property so that we are not querying information about the client
     * until the point in time where the foundation requests it. This prevents scenarios where
     * client-side feature-detection may happen too early, such as when components are rendered on the server
     * and then initialized at mount time on the client.
     */
    MDCRippleFoundation.prototype.supportsPressRipple = function () {
        return this.adapter.browserSupportsCssVars();
    };
    MDCRippleFoundation.prototype.defaultActivationState = function () {
        return {
            activationEvent: undefined,
            hasDeactivationUXRun: false,
            isActivated: false,
            isProgrammatic: false,
            wasActivatedByPointer: false,
            wasElementMadeActive: false,
        };
    };
    /**
     * supportsPressRipple Passed from init to save a redundant function call
     */
    MDCRippleFoundation.prototype.registerRootHandlers = function (supportsPressRipple) {
        var e_1, _a;
        if (supportsPressRipple) {
            try {
                for (var ACTIVATION_EVENT_TYPES_1 = __values(ACTIVATION_EVENT_TYPES), ACTIVATION_EVENT_TYPES_1_1 = ACTIVATION_EVENT_TYPES_1.next(); !ACTIVATION_EVENT_TYPES_1_1.done; ACTIVATION_EVENT_TYPES_1_1 = ACTIVATION_EVENT_TYPES_1.next()) {
                    var evtType = ACTIVATION_EVENT_TYPES_1_1.value;
                    this.adapter.registerInteractionHandler(evtType, this.activateHandler);
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (ACTIVATION_EVENT_TYPES_1_1 && !ACTIVATION_EVENT_TYPES_1_1.done && (_a = ACTIVATION_EVENT_TYPES_1.return)) _a.call(ACTIVATION_EVENT_TYPES_1);
                }
                finally { if (e_1) throw e_1.error; }
            }
            if (this.adapter.isUnbounded()) {
                this.adapter.registerResizeHandler(this.resizeHandler);
            }
        }
        this.adapter.registerInteractionHandler('focus', this.focusHandler);
        this.adapter.registerInteractionHandler('blur', this.blurHandler);
    };
    MDCRippleFoundation.prototype.registerDeactivationHandlers = function (evt) {
        var e_2, _a;
        if (evt.type === 'keydown') {
            this.adapter.registerInteractionHandler('keyup', this.deactivateHandler);
        }
        else {
            try {
                for (var POINTER_DEACTIVATION_EVENT_TYPES_1 = __values(POINTER_DEACTIVATION_EVENT_TYPES), POINTER_DEACTIVATION_EVENT_TYPES_1_1 = POINTER_DEACTIVATION_EVENT_TYPES_1.next(); !POINTER_DEACTIVATION_EVENT_TYPES_1_1.done; POINTER_DEACTIVATION_EVENT_TYPES_1_1 = POINTER_DEACTIVATION_EVENT_TYPES_1.next()) {
                    var evtType = POINTER_DEACTIVATION_EVENT_TYPES_1_1.value;
                    this.adapter.registerDocumentInteractionHandler(evtType, this.deactivateHandler);
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (POINTER_DEACTIVATION_EVENT_TYPES_1_1 && !POINTER_DEACTIVATION_EVENT_TYPES_1_1.done && (_a = POINTER_DEACTIVATION_EVENT_TYPES_1.return)) _a.call(POINTER_DEACTIVATION_EVENT_TYPES_1);
                }
                finally { if (e_2) throw e_2.error; }
            }
        }
    };
    MDCRippleFoundation.prototype.deregisterRootHandlers = function () {
        var e_3, _a;
        try {
            for (var ACTIVATION_EVENT_TYPES_2 = __values(ACTIVATION_EVENT_TYPES), ACTIVATION_EVENT_TYPES_2_1 = ACTIVATION_EVENT_TYPES_2.next(); !ACTIVATION_EVENT_TYPES_2_1.done; ACTIVATION_EVENT_TYPES_2_1 = ACTIVATION_EVENT_TYPES_2.next()) {
                var evtType = ACTIVATION_EVENT_TYPES_2_1.value;
                this.adapter.deregisterInteractionHandler(evtType, this.activateHandler);
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (ACTIVATION_EVENT_TYPES_2_1 && !ACTIVATION_EVENT_TYPES_2_1.done && (_a = ACTIVATION_EVENT_TYPES_2.return)) _a.call(ACTIVATION_EVENT_TYPES_2);
            }
            finally { if (e_3) throw e_3.error; }
        }
        this.adapter.deregisterInteractionHandler('focus', this.focusHandler);
        this.adapter.deregisterInteractionHandler('blur', this.blurHandler);
        if (this.adapter.isUnbounded()) {
            this.adapter.deregisterResizeHandler(this.resizeHandler);
        }
    };
    MDCRippleFoundation.prototype.deregisterDeactivationHandlers = function () {
        var e_4, _a;
        this.adapter.deregisterInteractionHandler('keyup', this.deactivateHandler);
        try {
            for (var POINTER_DEACTIVATION_EVENT_TYPES_2 = __values(POINTER_DEACTIVATION_EVENT_TYPES), POINTER_DEACTIVATION_EVENT_TYPES_2_1 = POINTER_DEACTIVATION_EVENT_TYPES_2.next(); !POINTER_DEACTIVATION_EVENT_TYPES_2_1.done; POINTER_DEACTIVATION_EVENT_TYPES_2_1 = POINTER_DEACTIVATION_EVENT_TYPES_2.next()) {
                var evtType = POINTER_DEACTIVATION_EVENT_TYPES_2_1.value;
                this.adapter.deregisterDocumentInteractionHandler(evtType, this.deactivateHandler);
            }
        }
        catch (e_4_1) { e_4 = { error: e_4_1 }; }
        finally {
            try {
                if (POINTER_DEACTIVATION_EVENT_TYPES_2_1 && !POINTER_DEACTIVATION_EVENT_TYPES_2_1.done && (_a = POINTER_DEACTIVATION_EVENT_TYPES_2.return)) _a.call(POINTER_DEACTIVATION_EVENT_TYPES_2);
            }
            finally { if (e_4) throw e_4.error; }
        }
    };
    MDCRippleFoundation.prototype.removeCssVars = function () {
        var _this = this;
        var rippleStrings = MDCRippleFoundation.strings;
        var keys = Object.keys(rippleStrings);
        keys.forEach(function (key) {
            if (key.indexOf('VAR_') === 0) {
                _this.adapter.updateCssVariable(rippleStrings[key], null);
            }
        });
    };
    MDCRippleFoundation.prototype.activateImpl = function (evt) {
        var _this = this;
        if (this.adapter.isSurfaceDisabled()) {
            return;
        }
        var activationState = this.activationState;
        if (activationState.isActivated) {
            return;
        }
        // Avoid reacting to follow-on events fired by touch device after an already-processed user interaction
        var previousActivationEvent = this.previousActivationEvent;
        var isSameInteraction = previousActivationEvent && evt !== undefined && previousActivationEvent.type !== evt.type;
        if (isSameInteraction) {
            return;
        }
        activationState.isActivated = true;
        activationState.isProgrammatic = evt === undefined;
        activationState.activationEvent = evt;
        activationState.wasActivatedByPointer = activationState.isProgrammatic ? false : evt !== undefined && (evt.type === 'mousedown' || evt.type === 'touchstart' || evt.type === 'pointerdown');
        var hasActivatedChild = evt !== undefined &&
            activatedTargets.length > 0 &&
            activatedTargets.some(function (target) { return _this.adapter.containsEventTarget(target); });
        if (hasActivatedChild) {
            // Immediately reset activation state, while preserving logic that prevents touch follow-on events
            this.resetActivationState();
            return;
        }
        if (evt !== undefined) {
            activatedTargets.push(evt.target);
            this.registerDeactivationHandlers(evt);
        }
        activationState.wasElementMadeActive = this.checkElementMadeActive(evt);
        if (activationState.wasElementMadeActive) {
            this.animateActivation();
        }
        requestAnimationFrame(function () {
            // Reset array on next frame after the current event has had a chance to bubble to prevent ancestor ripples
            activatedTargets = [];
            if (!activationState.wasElementMadeActive
                && evt !== undefined
                && (evt.key === ' ' || evt.keyCode === 32)) {
                // If space was pressed, try again within an rAF call to detect :active, because different UAs report
                // active states inconsistently when they're called within event handling code:
                // - https://bugs.chromium.org/p/chromium/issues/detail?id=635971
                // - https://bugzilla.mozilla.org/show_bug.cgi?id=1293741
                // We try first outside rAF to support Edge, which does not exhibit this problem, but will crash if a CSS
                // variable is set within a rAF callback for a submit button interaction (#2241).
                activationState.wasElementMadeActive = _this.checkElementMadeActive(evt);
                if (activationState.wasElementMadeActive) {
                    _this.animateActivation();
                }
            }
            if (!activationState.wasElementMadeActive) {
                // Reset activation state immediately if element was not made active.
                _this.activationState = _this.defaultActivationState();
            }
        });
    };
    MDCRippleFoundation.prototype.checkElementMadeActive = function (evt) {
        return (evt !== undefined && evt.type === 'keydown') ?
            this.adapter.isSurfaceActive() :
            true;
    };
    MDCRippleFoundation.prototype.animateActivation = function () {
        var _this = this;
        var _a = MDCRippleFoundation.strings, VAR_FG_TRANSLATE_START = _a.VAR_FG_TRANSLATE_START, VAR_FG_TRANSLATE_END = _a.VAR_FG_TRANSLATE_END;
        var _b = MDCRippleFoundation.cssClasses, FG_DEACTIVATION = _b.FG_DEACTIVATION, FG_ACTIVATION = _b.FG_ACTIVATION;
        var DEACTIVATION_TIMEOUT_MS = MDCRippleFoundation.numbers.DEACTIVATION_TIMEOUT_MS;
        this.layoutInternal();
        var translateStart = '';
        var translateEnd = '';
        if (!this.adapter.isUnbounded()) {
            var _c = this.getFgTranslationCoordinates(), startPoint = _c.startPoint, endPoint = _c.endPoint;
            translateStart = startPoint.x + "px, " + startPoint.y + "px";
            translateEnd = endPoint.x + "px, " + endPoint.y + "px";
        }
        this.adapter.updateCssVariable(VAR_FG_TRANSLATE_START, translateStart);
        this.adapter.updateCssVariable(VAR_FG_TRANSLATE_END, translateEnd);
        // Cancel any ongoing activation/deactivation animations
        clearTimeout(this.activationTimer);
        clearTimeout(this.fgDeactivationRemovalTimer);
        this.rmBoundedActivationClasses();
        this.adapter.removeClass(FG_DEACTIVATION);
        // Force layout in order to re-trigger the animation.
        this.adapter.computeBoundingRect();
        this.adapter.addClass(FG_ACTIVATION);
        this.activationTimer = setTimeout(function () {
            _this.activationTimerCallback();
        }, DEACTIVATION_TIMEOUT_MS);
    };
    MDCRippleFoundation.prototype.getFgTranslationCoordinates = function () {
        var _a = this.activationState, activationEvent = _a.activationEvent, wasActivatedByPointer = _a.wasActivatedByPointer;
        var startPoint;
        if (wasActivatedByPointer) {
            startPoint = getNormalizedEventCoords(activationEvent, this.adapter.getWindowPageOffset(), this.adapter.computeBoundingRect());
        }
        else {
            startPoint = {
                x: this.frame.width / 2,
                y: this.frame.height / 2,
            };
        }
        // Center the element around the start point.
        startPoint = {
            x: startPoint.x - (this.initialSize / 2),
            y: startPoint.y - (this.initialSize / 2),
        };
        var endPoint = {
            x: (this.frame.width / 2) - (this.initialSize / 2),
            y: (this.frame.height / 2) - (this.initialSize / 2),
        };
        return { startPoint: startPoint, endPoint: endPoint };
    };
    MDCRippleFoundation.prototype.runDeactivationUXLogicIfReady = function () {
        var _this = this;
        // This method is called both when a pointing device is released, and when the activation animation ends.
        // The deactivation animation should only run after both of those occur.
        var FG_DEACTIVATION = MDCRippleFoundation.cssClasses.FG_DEACTIVATION;
        var _a = this.activationState, hasDeactivationUXRun = _a.hasDeactivationUXRun, isActivated = _a.isActivated;
        var activationHasEnded = hasDeactivationUXRun || !isActivated;
        if (activationHasEnded && this.activationAnimationHasEnded) {
            this.rmBoundedActivationClasses();
            this.adapter.addClass(FG_DEACTIVATION);
            this.fgDeactivationRemovalTimer = setTimeout(function () {
                _this.adapter.removeClass(FG_DEACTIVATION);
            }, numbers.FG_DEACTIVATION_MS);
        }
    };
    MDCRippleFoundation.prototype.rmBoundedActivationClasses = function () {
        var FG_ACTIVATION = MDCRippleFoundation.cssClasses.FG_ACTIVATION;
        this.adapter.removeClass(FG_ACTIVATION);
        this.activationAnimationHasEnded = false;
        this.adapter.computeBoundingRect();
    };
    MDCRippleFoundation.prototype.resetActivationState = function () {
        var _this = this;
        this.previousActivationEvent = this.activationState.activationEvent;
        this.activationState = this.defaultActivationState();
        // Touch devices may fire additional events for the same interaction within a short time.
        // Store the previous event until it's safe to assume that subsequent events are for new interactions.
        setTimeout(function () { return _this.previousActivationEvent = undefined; }, MDCRippleFoundation.numbers.TAP_DELAY_MS);
    };
    MDCRippleFoundation.prototype.deactivateImpl = function () {
        var _this = this;
        var activationState = this.activationState;
        // This can happen in scenarios such as when you have a keyup event that blurs the element.
        if (!activationState.isActivated) {
            return;
        }
        var state = __assign({}, activationState);
        if (activationState.isProgrammatic) {
            requestAnimationFrame(function () {
                _this.animateDeactivation(state);
            });
            this.resetActivationState();
        }
        else {
            this.deregisterDeactivationHandlers();
            requestAnimationFrame(function () {
                _this.activationState.hasDeactivationUXRun = true;
                _this.animateDeactivation(state);
                _this.resetActivationState();
            });
        }
    };
    MDCRippleFoundation.prototype.animateDeactivation = function (_a) {
        var wasActivatedByPointer = _a.wasActivatedByPointer, wasElementMadeActive = _a.wasElementMadeActive;
        if (wasActivatedByPointer || wasElementMadeActive) {
            this.runDeactivationUXLogicIfReady();
        }
    };
    MDCRippleFoundation.prototype.layoutInternal = function () {
        var _this = this;
        this.frame = this.adapter.computeBoundingRect();
        var maxDim = Math.max(this.frame.height, this.frame.width);
        // Surface diameter is treated differently for unbounded vs. bounded ripples.
        // Unbounded ripple diameter is calculated smaller since the surface is expected to already be padded appropriately
        // to extend the hitbox, and the ripple is expected to meet the edges of the padded hitbox (which is typically
        // square). Bounded ripples, on the other hand, are fully expected to expand beyond the surface's longest diameter
        // (calculated based on the diagonal plus a constant padding), and are clipped at the surface's border via
        // `overflow: hidden`.
        var getBoundedRadius = function () {
            var hypotenuse = Math.sqrt(Math.pow(_this.frame.width, 2) + Math.pow(_this.frame.height, 2));
            return hypotenuse + MDCRippleFoundation.numbers.PADDING;
        };
        this.maxRadius = this.adapter.isUnbounded() ? maxDim : getBoundedRadius();
        // Ripple is sized as a fraction of the largest dimension of the surface, then scales up using a CSS scale transform
        var initialSize = Math.floor(maxDim * MDCRippleFoundation.numbers.INITIAL_ORIGIN_SCALE);
        // Unbounded ripple size should always be even number to equally center align.
        if (this.adapter.isUnbounded() && initialSize % 2 !== 0) {
            this.initialSize = initialSize - 1;
        }
        else {
            this.initialSize = initialSize;
        }
        this.fgScale = "" + this.maxRadius / this.initialSize;
        this.updateLayoutCssVars();
    };
    MDCRippleFoundation.prototype.updateLayoutCssVars = function () {
        var _a = MDCRippleFoundation.strings, VAR_FG_SIZE = _a.VAR_FG_SIZE, VAR_LEFT = _a.VAR_LEFT, VAR_TOP = _a.VAR_TOP, VAR_FG_SCALE = _a.VAR_FG_SCALE;
        this.adapter.updateCssVariable(VAR_FG_SIZE, this.initialSize + "px");
        this.adapter.updateCssVariable(VAR_FG_SCALE, this.fgScale);
        if (this.adapter.isUnbounded()) {
            this.unboundedCoords = {
                left: Math.round((this.frame.width / 2) - (this.initialSize / 2)),
                top: Math.round((this.frame.height / 2) - (this.initialSize / 2)),
            };
            this.adapter.updateCssVariable(VAR_LEFT, this.unboundedCoords.left + "px");
            this.adapter.updateCssVariable(VAR_TOP, this.unboundedCoords.top + "px");
        }
    };
    return MDCRippleFoundation;
}(MDCFoundation));
// tslint:disable-next-line:no-default-export Needed for backward compatibility with MDC Web v0.44.0 and earlier.
var MDCRippleFoundation$1 = MDCRippleFoundation;

/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const t={ATTRIBUTE:1,CHILD:2,PROPERTY:3,BOOLEAN_ATTRIBUTE:4,EVENT:5,ELEMENT:6},e=t=>(...e)=>({_$litDirective$:t,values:e});let i$1 = class i{constructor(t){}get _$AU(){return this._$AM._$AU}_$AT(t,e,i){this._$Ct=t,this._$AM=e,this._$Ci=i;}_$AS(t,e){return this.update(t,e)}update(t,e){return this.render(...e)}};

/**
 * @license
 * Copyright 2018 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const o=e(class extends i$1{constructor(t$1){var i;if(super(t$1),t$1.type!==t.ATTRIBUTE||"class"!==t$1.name||(null===(i=t$1.strings)||void 0===i?void 0:i.length)>2)throw Error("`classMap()` can only be used in the `class` attribute and must be the only part in the attribute.")}render(t){return " "+Object.keys(t).filter((i=>t[i])).join(" ")+" "}update(i,[s]){var r,o;if(void 0===this.nt){this.nt=new Set,void 0!==i.strings&&(this.st=new Set(i.strings.join(" ").split(/\s/).filter((t=>""!==t))));for(const t in s)s[t]&&!(null===(r=this.st)||void 0===r?void 0:r.has(t))&&this.nt.add(t);return this.render(s)}const e=i.element.classList;this.nt.forEach((t=>{t in s||(e.remove(t),this.nt.delete(t));}));for(const t in s){const i=!!s[t];i===this.nt.has(t)||(null===(o=this.st)||void 0===o?void 0:o.has(t))||(i?(e.add(t),this.nt.add(t)):(e.remove(t),this.nt.delete(t)));}return T}});

/**
 * @license
 * Copyright 2018 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const i=e(class extends i$1{constructor(t$1){var e;if(super(t$1),t$1.type!==t.ATTRIBUTE||"style"!==t$1.name||(null===(e=t$1.strings)||void 0===e?void 0:e.length)>2)throw Error("The `styleMap` directive must be used in the `style` attribute and must be the only part in the attribute.")}render(t){return Object.keys(t).reduce(((e,r)=>{const s=t[r];return null==s?e:e+`${r=r.replace(/(?:^(webkit|moz|ms|o)|)(?=[A-Z])/g,"-$&").toLowerCase()}:${s};`}),"")}update(e,[r]){const{style:s}=e.element;if(void 0===this.vt){this.vt=new Set;for(const t in r)this.vt.add(t);return this.render(r)}this.vt.forEach((t=>{null==r[t]&&(this.vt.delete(t),t.includes("-")?s.removeProperty(t):s[t]="");}));for(const t in r){const e=r[t];null!=e&&(this.vt.add(t),t.includes("-")?s.setProperty(t,e):s[t]=e);}return T}});

/**
 * @license
 * Copyright 2018 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
/** @soyCompatible */
class RippleBase extends BaseElement {
    constructor() {
        super(...arguments);
        this.primary = false;
        this.accent = false;
        this.unbounded = false;
        this.disabled = false;
        this.activated = false;
        this.selected = false;
        this.internalUseStateLayerCustomProperties = false;
        this.hovering = false;
        this.bgFocused = false;
        this.fgActivation = false;
        this.fgDeactivation = false;
        this.fgScale = '';
        this.fgSize = '';
        this.translateStart = '';
        this.translateEnd = '';
        this.leftPos = '';
        this.topPos = '';
        this.mdcFoundationClass = MDCRippleFoundation$1;
    }
    get isActive() {
        return matches(this.parentElement || this, ':active');
    }
    createAdapter() {
        return {
            browserSupportsCssVars: () => true,
            isUnbounded: () => this.unbounded,
            isSurfaceActive: () => this.isActive,
            isSurfaceDisabled: () => this.disabled,
            addClass: (className) => {
                switch (className) {
                    case 'mdc-ripple-upgraded--background-focused':
                        this.bgFocused = true;
                        break;
                    case 'mdc-ripple-upgraded--foreground-activation':
                        this.fgActivation = true;
                        break;
                    case 'mdc-ripple-upgraded--foreground-deactivation':
                        this.fgDeactivation = true;
                        break;
                }
            },
            removeClass: (className) => {
                switch (className) {
                    case 'mdc-ripple-upgraded--background-focused':
                        this.bgFocused = false;
                        break;
                    case 'mdc-ripple-upgraded--foreground-activation':
                        this.fgActivation = false;
                        break;
                    case 'mdc-ripple-upgraded--foreground-deactivation':
                        this.fgDeactivation = false;
                        break;
                }
            },
            containsEventTarget: () => true,
            registerInteractionHandler: () => undefined,
            deregisterInteractionHandler: () => undefined,
            registerDocumentInteractionHandler: () => undefined,
            deregisterDocumentInteractionHandler: () => undefined,
            registerResizeHandler: () => undefined,
            deregisterResizeHandler: () => undefined,
            updateCssVariable: (varName, value) => {
                switch (varName) {
                    case '--mdc-ripple-fg-scale':
                        this.fgScale = value;
                        break;
                    case '--mdc-ripple-fg-size':
                        this.fgSize = value;
                        break;
                    case '--mdc-ripple-fg-translate-end':
                        this.translateEnd = value;
                        break;
                    case '--mdc-ripple-fg-translate-start':
                        this.translateStart = value;
                        break;
                    case '--mdc-ripple-left':
                        this.leftPos = value;
                        break;
                    case '--mdc-ripple-top':
                        this.topPos = value;
                        break;
                }
            },
            computeBoundingRect: () => (this.parentElement || this).getBoundingClientRect(),
            getWindowPageOffset: () => ({ x: window.pageXOffset, y: window.pageYOffset }),
        };
    }
    startPress(ev) {
        this.waitForFoundation(() => {
            this.mdcFoundation.activate(ev);
        });
    }
    endPress() {
        this.waitForFoundation(() => {
            this.mdcFoundation.deactivate();
        });
    }
    startFocus() {
        this.waitForFoundation(() => {
            this.mdcFoundation.handleFocus();
        });
    }
    endFocus() {
        this.waitForFoundation(() => {
            this.mdcFoundation.handleBlur();
        });
    }
    startHover() {
        this.hovering = true;
    }
    endHover() {
        this.hovering = false;
    }
    /**
     * Wait for the MDCFoundation to be created by `firstUpdated`
     */
    waitForFoundation(fn) {
        if (this.mdcFoundation) {
            fn();
        }
        else {
            this.updateComplete.then(fn);
        }
    }
    update(changedProperties) {
        if (changedProperties.has('disabled')) {
            // stop hovering when ripple is disabled to prevent a stuck "hover" state
            // When re-enabled, the outer component will get a `mouseenter` event on
            // the first movement, which will call `startHover()`
            if (this.disabled) {
                this.endHover();
            }
        }
        super.update(changedProperties);
    }
    /** @soyTemplate */
    render() {
        const shouldActivateInPrimary = this.activated && (this.primary || !this.accent);
        const shouldSelectInPrimary = this.selected && (this.primary || !this.accent);
        /** @classMap */
        const classes = {
            'mdc-ripple-surface--accent': this.accent,
            'mdc-ripple-surface--primary--activated': shouldActivateInPrimary,
            'mdc-ripple-surface--accent--activated': this.accent && this.activated,
            'mdc-ripple-surface--primary--selected': shouldSelectInPrimary,
            'mdc-ripple-surface--accent--selected': this.accent && this.selected,
            'mdc-ripple-surface--disabled': this.disabled,
            'mdc-ripple-surface--hover': this.hovering,
            'mdc-ripple-surface--primary': this.primary,
            'mdc-ripple-surface--selected': this.selected,
            'mdc-ripple-upgraded--background-focused': this.bgFocused,
            'mdc-ripple-upgraded--foreground-activation': this.fgActivation,
            'mdc-ripple-upgraded--foreground-deactivation': this.fgDeactivation,
            'mdc-ripple-upgraded--unbounded': this.unbounded,
            'mdc-ripple-surface--internal-use-state-layer-custom-properties': this.internalUseStateLayerCustomProperties,
        };
        return x `
        <div class="mdc-ripple-surface mdc-ripple-upgraded ${o(classes)}"
          style="${i({
            '--mdc-ripple-fg-scale': this.fgScale,
            '--mdc-ripple-fg-size': this.fgSize,
            '--mdc-ripple-fg-translate-end': this.translateEnd,
            '--mdc-ripple-fg-translate-start': this.translateStart,
            '--mdc-ripple-left': this.leftPos,
            '--mdc-ripple-top': this.topPos,
        })}"></div>`;
    }
}
__decorate([
    i$4('.mdc-ripple-surface')
], RippleBase.prototype, "mdcRoot", void 0);
__decorate([
    e$6({ type: Boolean })
], RippleBase.prototype, "primary", void 0);
__decorate([
    e$6({ type: Boolean })
], RippleBase.prototype, "accent", void 0);
__decorate([
    e$6({ type: Boolean })
], RippleBase.prototype, "unbounded", void 0);
__decorate([
    e$6({ type: Boolean })
], RippleBase.prototype, "disabled", void 0);
__decorate([
    e$6({ type: Boolean })
], RippleBase.prototype, "activated", void 0);
__decorate([
    e$6({ type: Boolean })
], RippleBase.prototype, "selected", void 0);
__decorate([
    e$6({ type: Boolean })
], RippleBase.prototype, "internalUseStateLayerCustomProperties", void 0);
__decorate([
    t$3()
], RippleBase.prototype, "hovering", void 0);
__decorate([
    t$3()
], RippleBase.prototype, "bgFocused", void 0);
__decorate([
    t$3()
], RippleBase.prototype, "fgActivation", void 0);
__decorate([
    t$3()
], RippleBase.prototype, "fgDeactivation", void 0);
__decorate([
    t$3()
], RippleBase.prototype, "fgScale", void 0);
__decorate([
    t$3()
], RippleBase.prototype, "fgSize", void 0);
__decorate([
    t$3()
], RippleBase.prototype, "translateStart", void 0);
__decorate([
    t$3()
], RippleBase.prototype, "translateEnd", void 0);
__decorate([
    t$3()
], RippleBase.prototype, "leftPos", void 0);
__decorate([
    t$3()
], RippleBase.prototype, "topPos", void 0);

/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-LIcense-Identifier: Apache-2.0
 */
const styles$2 = i$3 `.mdc-ripple-surface{--mdc-ripple-fg-size: 0;--mdc-ripple-left: 0;--mdc-ripple-top: 0;--mdc-ripple-fg-scale: 1;--mdc-ripple-fg-translate-end: 0;--mdc-ripple-fg-translate-start: 0;-webkit-tap-highlight-color:rgba(0,0,0,0);will-change:transform,opacity;position:relative;outline:none;overflow:hidden}.mdc-ripple-surface::before,.mdc-ripple-surface::after{position:absolute;border-radius:50%;opacity:0;pointer-events:none;content:""}.mdc-ripple-surface::before{transition:opacity 15ms linear,background-color 15ms linear;z-index:1;z-index:var(--mdc-ripple-z-index, 1)}.mdc-ripple-surface::after{z-index:0;z-index:var(--mdc-ripple-z-index, 0)}.mdc-ripple-surface.mdc-ripple-upgraded::before{transform:scale(var(--mdc-ripple-fg-scale, 1))}.mdc-ripple-surface.mdc-ripple-upgraded::after{top:0;left:0;transform:scale(0);transform-origin:center center}.mdc-ripple-surface.mdc-ripple-upgraded--unbounded::after{top:var(--mdc-ripple-top, 0);left:var(--mdc-ripple-left, 0)}.mdc-ripple-surface.mdc-ripple-upgraded--foreground-activation::after{animation:mdc-ripple-fg-radius-in 225ms forwards,mdc-ripple-fg-opacity-in 75ms forwards}.mdc-ripple-surface.mdc-ripple-upgraded--foreground-deactivation::after{animation:mdc-ripple-fg-opacity-out 150ms;transform:translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))}.mdc-ripple-surface::before,.mdc-ripple-surface::after{top:calc(50% - 100%);left:calc(50% - 100%);width:200%;height:200%}.mdc-ripple-surface.mdc-ripple-upgraded::after{width:var(--mdc-ripple-fg-size, 100%);height:var(--mdc-ripple-fg-size, 100%)}.mdc-ripple-surface[data-mdc-ripple-is-unbounded],.mdc-ripple-upgraded--unbounded{overflow:visible}.mdc-ripple-surface[data-mdc-ripple-is-unbounded]::before,.mdc-ripple-surface[data-mdc-ripple-is-unbounded]::after,.mdc-ripple-upgraded--unbounded::before,.mdc-ripple-upgraded--unbounded::after{top:calc(50% - 50%);left:calc(50% - 50%);width:100%;height:100%}.mdc-ripple-surface[data-mdc-ripple-is-unbounded].mdc-ripple-upgraded::before,.mdc-ripple-surface[data-mdc-ripple-is-unbounded].mdc-ripple-upgraded::after,.mdc-ripple-upgraded--unbounded.mdc-ripple-upgraded::before,.mdc-ripple-upgraded--unbounded.mdc-ripple-upgraded::after{top:var(--mdc-ripple-top, calc(50% - 50%));left:var(--mdc-ripple-left, calc(50% - 50%));width:var(--mdc-ripple-fg-size, 100%);height:var(--mdc-ripple-fg-size, 100%)}.mdc-ripple-surface[data-mdc-ripple-is-unbounded].mdc-ripple-upgraded::after,.mdc-ripple-upgraded--unbounded.mdc-ripple-upgraded::after{width:var(--mdc-ripple-fg-size, 100%);height:var(--mdc-ripple-fg-size, 100%)}.mdc-ripple-surface::before,.mdc-ripple-surface::after{background-color:#000;background-color:var(--mdc-ripple-color, #000)}.mdc-ripple-surface:hover::before,.mdc-ripple-surface.mdc-ripple-surface--hover::before{opacity:0.04;opacity:var(--mdc-ripple-hover-opacity, 0.04)}.mdc-ripple-surface.mdc-ripple-upgraded--background-focused::before,.mdc-ripple-surface:not(.mdc-ripple-upgraded):focus::before{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-focus-opacity, 0.12)}.mdc-ripple-surface:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-ripple-surface:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-ripple-surface.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.12)}@keyframes mdc-ripple-fg-radius-in{from{animation-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transform:translate(var(--mdc-ripple-fg-translate-start, 0)) scale(1)}to{transform:translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))}}@keyframes mdc-ripple-fg-opacity-in{from{animation-timing-function:linear;opacity:0}to{opacity:var(--mdc-ripple-fg-opacity, 0)}}@keyframes mdc-ripple-fg-opacity-out{from{animation-timing-function:linear;opacity:var(--mdc-ripple-fg-opacity, 0)}to{opacity:0}}:host{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;display:block}:host .mdc-ripple-surface{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;will-change:unset}.mdc-ripple-surface--primary::before,.mdc-ripple-surface--primary::after{background-color:#6200ee;background-color:var(--mdc-ripple-color, var(--mdc-theme-primary, #6200ee))}.mdc-ripple-surface--primary:hover::before,.mdc-ripple-surface--primary.mdc-ripple-surface--hover::before{opacity:0.04;opacity:var(--mdc-ripple-hover-opacity, 0.04)}.mdc-ripple-surface--primary.mdc-ripple-upgraded--background-focused::before,.mdc-ripple-surface--primary:not(.mdc-ripple-upgraded):focus::before{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-focus-opacity, 0.12)}.mdc-ripple-surface--primary:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-ripple-surface--primary:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-ripple-surface--primary.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-ripple-surface--primary--activated::before{opacity:0.12;opacity:var(--mdc-ripple-activated-opacity, 0.12)}.mdc-ripple-surface--primary--activated::before,.mdc-ripple-surface--primary--activated::after{background-color:#6200ee;background-color:var(--mdc-ripple-color, var(--mdc-theme-primary, #6200ee))}.mdc-ripple-surface--primary--activated:hover::before,.mdc-ripple-surface--primary--activated.mdc-ripple-surface--hover::before{opacity:0.16;opacity:var(--mdc-ripple-hover-opacity, 0.16)}.mdc-ripple-surface--primary--activated.mdc-ripple-upgraded--background-focused::before,.mdc-ripple-surface--primary--activated:not(.mdc-ripple-upgraded):focus::before{transition-duration:75ms;opacity:0.24;opacity:var(--mdc-ripple-focus-opacity, 0.24)}.mdc-ripple-surface--primary--activated:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-ripple-surface--primary--activated:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:0.24;opacity:var(--mdc-ripple-press-opacity, 0.24)}.mdc-ripple-surface--primary--activated.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.24)}.mdc-ripple-surface--primary--selected::before{opacity:0.08;opacity:var(--mdc-ripple-selected-opacity, 0.08)}.mdc-ripple-surface--primary--selected::before,.mdc-ripple-surface--primary--selected::after{background-color:#6200ee;background-color:var(--mdc-ripple-color, var(--mdc-theme-primary, #6200ee))}.mdc-ripple-surface--primary--selected:hover::before,.mdc-ripple-surface--primary--selected.mdc-ripple-surface--hover::before{opacity:0.12;opacity:var(--mdc-ripple-hover-opacity, 0.12)}.mdc-ripple-surface--primary--selected.mdc-ripple-upgraded--background-focused::before,.mdc-ripple-surface--primary--selected:not(.mdc-ripple-upgraded):focus::before{transition-duration:75ms;opacity:0.2;opacity:var(--mdc-ripple-focus-opacity, 0.2)}.mdc-ripple-surface--primary--selected:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-ripple-surface--primary--selected:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:0.2;opacity:var(--mdc-ripple-press-opacity, 0.2)}.mdc-ripple-surface--primary--selected.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.2)}.mdc-ripple-surface--accent::before,.mdc-ripple-surface--accent::after{background-color:#018786;background-color:var(--mdc-ripple-color, var(--mdc-theme-secondary, #018786))}.mdc-ripple-surface--accent:hover::before,.mdc-ripple-surface--accent.mdc-ripple-surface--hover::before{opacity:0.04;opacity:var(--mdc-ripple-hover-opacity, 0.04)}.mdc-ripple-surface--accent.mdc-ripple-upgraded--background-focused::before,.mdc-ripple-surface--accent:not(.mdc-ripple-upgraded):focus::before{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-focus-opacity, 0.12)}.mdc-ripple-surface--accent:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-ripple-surface--accent:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-ripple-surface--accent.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.12)}.mdc-ripple-surface--accent--activated::before{opacity:0.12;opacity:var(--mdc-ripple-activated-opacity, 0.12)}.mdc-ripple-surface--accent--activated::before,.mdc-ripple-surface--accent--activated::after{background-color:#018786;background-color:var(--mdc-ripple-color, var(--mdc-theme-secondary, #018786))}.mdc-ripple-surface--accent--activated:hover::before,.mdc-ripple-surface--accent--activated.mdc-ripple-surface--hover::before{opacity:0.16;opacity:var(--mdc-ripple-hover-opacity, 0.16)}.mdc-ripple-surface--accent--activated.mdc-ripple-upgraded--background-focused::before,.mdc-ripple-surface--accent--activated:not(.mdc-ripple-upgraded):focus::before{transition-duration:75ms;opacity:0.24;opacity:var(--mdc-ripple-focus-opacity, 0.24)}.mdc-ripple-surface--accent--activated:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-ripple-surface--accent--activated:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:0.24;opacity:var(--mdc-ripple-press-opacity, 0.24)}.mdc-ripple-surface--accent--activated.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.24)}.mdc-ripple-surface--accent--selected::before{opacity:0.08;opacity:var(--mdc-ripple-selected-opacity, 0.08)}.mdc-ripple-surface--accent--selected::before,.mdc-ripple-surface--accent--selected::after{background-color:#018786;background-color:var(--mdc-ripple-color, var(--mdc-theme-secondary, #018786))}.mdc-ripple-surface--accent--selected:hover::before,.mdc-ripple-surface--accent--selected.mdc-ripple-surface--hover::before{opacity:0.12;opacity:var(--mdc-ripple-hover-opacity, 0.12)}.mdc-ripple-surface--accent--selected.mdc-ripple-upgraded--background-focused::before,.mdc-ripple-surface--accent--selected:not(.mdc-ripple-upgraded):focus::before{transition-duration:75ms;opacity:0.2;opacity:var(--mdc-ripple-focus-opacity, 0.2)}.mdc-ripple-surface--accent--selected:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-ripple-surface--accent--selected:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:0.2;opacity:var(--mdc-ripple-press-opacity, 0.2)}.mdc-ripple-surface--accent--selected.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-press-opacity, 0.2)}.mdc-ripple-surface--disabled{opacity:0}.mdc-ripple-surface--internal-use-state-layer-custom-properties::before,.mdc-ripple-surface--internal-use-state-layer-custom-properties::after{background-color:#000;background-color:var(--mdc-ripple-hover-state-layer-color, #000)}.mdc-ripple-surface--internal-use-state-layer-custom-properties:hover::before,.mdc-ripple-surface--internal-use-state-layer-custom-properties.mdc-ripple-surface--hover::before{opacity:0.04;opacity:var(--mdc-ripple-hover-state-layer-opacity, 0.04)}.mdc-ripple-surface--internal-use-state-layer-custom-properties.mdc-ripple-upgraded--background-focused::before,.mdc-ripple-surface--internal-use-state-layer-custom-properties:not(.mdc-ripple-upgraded):focus::before{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-focus-state-layer-opacity, 0.12)}.mdc-ripple-surface--internal-use-state-layer-custom-properties:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-ripple-surface--internal-use-state-layer-custom-properties:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:0.12;opacity:var(--mdc-ripple-pressed-state-layer-opacity, 0.12)}.mdc-ripple-surface--internal-use-state-layer-custom-properties.mdc-ripple-upgraded{--mdc-ripple-fg-opacity:var(--mdc-ripple-pressed-state-layer-opacity, 0.12)}`;

/**
 * @license
 * Copyright 2018 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
/** @soyCompatible */
let Ripple = class Ripple extends RippleBase {
};
Ripple.styles = [styles$2];
Ripple = __decorate([
    e$7('mwc-ripple')
], Ripple);

/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
/**
 * TypeScript version of the decorator
 * @see https://www.typescriptlang.org/docs/handbook/decorators.html#property-decorators
 */
function tsDecorator(prototype, name, descriptor) {
    const constructor = prototype.constructor;
    if (!descriptor) {
        /**
         * lit uses internal properties with two leading underscores to
         * provide storage for accessors
         */
        const litInternalPropertyKey = `__${name}`;
        descriptor =
            constructor.getPropertyDescriptor(name, litInternalPropertyKey);
        if (!descriptor) {
            throw new Error('@ariaProperty must be used after a @property decorator');
        }
    }
    // descriptor must exist at this point, reassign so typescript understands
    const propDescriptor = descriptor;
    let attribute = '';
    if (!propDescriptor.set) {
        throw new Error(`@ariaProperty requires a setter for ${name}`);
    }
    // TODO(b/202853219): Remove this check when internal tooling is
    // compatible
    // tslint:disable-next-line:no-any bail if applied to internal generated class
    if (prototype.dispatchWizEvent) {
        return descriptor;
    }
    const wrappedDescriptor = {
        configurable: true,
        enumerable: true,
        set(value) {
            if (attribute === '') {
                const options = constructor.getPropertyOptions(name);
                // if attribute is not a string, use `name` instead
                attribute =
                    typeof options.attribute === 'string' ? options.attribute : name;
            }
            if (this.hasAttribute(attribute)) {
                this.removeAttribute(attribute);
            }
            propDescriptor.set.call(this, value);
        }
    };
    if (propDescriptor.get) {
        wrappedDescriptor.get = function () {
            return propDescriptor.get.call(this);
        };
    }
    return wrappedDescriptor;
}
/**
 * A property decorator proxies an aria attribute to an internal node
 *
 * This decorator is only intended for use with ARIA attributes, such as `role`
 * and `aria-label` due to screenreader needs.
 *
 * Upon first render, `@ariaProperty` will remove the attribute from the host
 * element to prevent screenreaders from reading the host instead of the
 * internal node.
 *
 * This decorator should only be used for non-Symbol public fields decorated
 * with `@property`, or on a setter with an optional getter.
 *
 * @example
 * ```ts
 * class MyElement {
 *   @ariaProperty
 *   @property({ type: String, attribute: 'aria-label' })
 *   ariaLabel!: string;
 * }
 * ```
 * @category Decorator
 * @ExportDecoratedItems
 */
function ariaProperty(protoOrDescriptor, name, 
// tslint:disable-next-line:no-any any is required as a return type from decorators
descriptor) {
    if (name !== undefined) {
        return tsDecorator(protoOrDescriptor, name, descriptor);
    }
    else {
        throw new Error('@ariaProperty only supports TypeScript Decorators');
    }
}

/**
 * @license
 * Copyright 2020 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
/**
 * Class that encapsulates the events handlers for `mwc-ripple`
 *
 *
 * Example:
 * ```
 * class XFoo extends LitElement {
 *   async getRipple() {
 *     this.renderRipple = true;
 *     await this.updateComplete;
 *     return this.renderRoot.querySelector('mwc-ripple');
 *   }
 *   rippleHandlers = new RippleHandlers(() => this.getRipple());
 *
 *   render() {
 *     return html`
 *       <div @mousedown=${this.rippleHandlers.startPress}></div>
 *       ${this.renderRipple ? html`<mwc-ripple></mwc-ripple>` : ''}
 *     `;
 *   }
 * }
 * ```
 */
class RippleHandlers {
    constructor(
    /** Function that returns a `mwc-ripple` */
    rippleFn) {
        this.startPress = (ev) => {
            rippleFn().then((r) => {
                r && r.startPress(ev);
            });
        };
        this.endPress = () => {
            rippleFn().then((r) => {
                r && r.endPress();
            });
        };
        this.startFocus = () => {
            rippleFn().then((r) => {
                r && r.startFocus();
            });
        };
        this.endFocus = () => {
            rippleFn().then((r) => {
                r && r.endFocus();
            });
        };
        this.startHover = () => {
            rippleFn().then((r) => {
                r && r.startHover();
            });
        };
        this.endHover = () => {
            rippleFn().then((r) => {
                r && r.endHover();
            });
        };
    }
}

/**
 * @license
 * Copyright 2018 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const l=l=>null!=l?l:A;

/**
 * @license
 * Copyright 2018 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
/** @soyCompatible */
class IconButtonBase extends s {
    constructor() {
        super(...arguments);
        this.disabled = false;
        this.icon = '';
        this.shouldRenderRipple = false;
        this.rippleHandlers = new RippleHandlers(() => {
            this.shouldRenderRipple = true;
            return this.ripple;
        });
    }
    /** @soyTemplate */
    renderRipple() {
        return this.shouldRenderRipple ? x `
            <mwc-ripple
                .disabled="${this.disabled}"
                unbounded>
            </mwc-ripple>` :
            '';
    }
    focus() {
        const buttonElement = this.buttonElement;
        if (buttonElement) {
            this.rippleHandlers.startFocus();
            buttonElement.focus();
        }
    }
    blur() {
        const buttonElement = this.buttonElement;
        if (buttonElement) {
            this.rippleHandlers.endFocus();
            buttonElement.blur();
        }
    }
    /** @soyTemplate */
    render() {
        return x `<button
        class="mdc-icon-button mdc-icon-button--display-flex"
        aria-label="${this.ariaLabel || this.icon}"
        aria-haspopup="${l(this.ariaHasPopup)}"
        ?disabled="${this.disabled}"
        @focus="${this.handleRippleFocus}"
        @blur="${this.handleRippleBlur}"
        @mousedown="${this.handleRippleMouseDown}"
        @mouseenter="${this.handleRippleMouseEnter}"
        @mouseleave="${this.handleRippleMouseLeave}"
        @touchstart="${this.handleRippleTouchStart}"
        @touchend="${this.handleRippleDeactivate}"
        @touchcancel="${this.handleRippleDeactivate}"
    >${this.renderRipple()}
    ${this.icon ? x `<i class="material-icons">${this.icon}</i>` : ''}
    <span
      ><slot></slot
    ></span>
  </button>`;
    }
    handleRippleMouseDown(event) {
        const onUp = () => {
            window.removeEventListener('mouseup', onUp);
            this.handleRippleDeactivate();
        };
        window.addEventListener('mouseup', onUp);
        this.rippleHandlers.startPress(event);
    }
    handleRippleTouchStart(event) {
        this.rippleHandlers.startPress(event);
    }
    handleRippleDeactivate() {
        this.rippleHandlers.endPress();
    }
    handleRippleMouseEnter() {
        this.rippleHandlers.startHover();
    }
    handleRippleMouseLeave() {
        this.rippleHandlers.endHover();
    }
    handleRippleFocus() {
        this.rippleHandlers.startFocus();
    }
    handleRippleBlur() {
        this.rippleHandlers.endFocus();
    }
}
__decorate([
    e$6({ type: Boolean, reflect: true })
], IconButtonBase.prototype, "disabled", void 0);
__decorate([
    e$6({ type: String })
], IconButtonBase.prototype, "icon", void 0);
__decorate([
    ariaProperty,
    e$6({ type: String, attribute: 'aria-label' })
], IconButtonBase.prototype, "ariaLabel", void 0);
__decorate([
    ariaProperty,
    e$6({ type: String, attribute: 'aria-haspopup' })
], IconButtonBase.prototype, "ariaHasPopup", void 0);
__decorate([
    i$4('button')
], IconButtonBase.prototype, "buttonElement", void 0);
__decorate([
    e$4('mwc-ripple')
], IconButtonBase.prototype, "ripple", void 0);
__decorate([
    t$3()
], IconButtonBase.prototype, "shouldRenderRipple", void 0);
__decorate([
    e$5({ passive: true })
], IconButtonBase.prototype, "handleRippleMouseDown", null);
__decorate([
    e$5({ passive: true })
], IconButtonBase.prototype, "handleRippleTouchStart", null);

/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-LIcense-Identifier: Apache-2.0
 */
const styles$1 = i$3 `.material-icons{font-family:var(--mdc-icon-font, "Material Icons");font-weight:normal;font-style:normal;font-size:var(--mdc-icon-size, 24px);line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;-moz-osx-font-smoothing:grayscale;font-feature-settings:"liga"}.mdc-icon-button{font-size:24px;width:48px;height:48px;padding:12px}.mdc-icon-button .mdc-icon-button__focus-ring{display:none}.mdc-icon-button.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring,.mdc-icon-button:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring{display:block;max-height:48px;max-width:48px}@media screen and (forced-colors: active){.mdc-icon-button.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring,.mdc-icon-button:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring{pointer-events:none;border:2px solid transparent;border-radius:6px;box-sizing:content-box;position:absolute;top:50%;left:50%;transform:translate(-50%, -50%);height:100%;width:100%}}@media screen and (forced-colors: active)and (forced-colors: active){.mdc-icon-button.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring,.mdc-icon-button:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring{border-color:CanvasText}}@media screen and (forced-colors: active){.mdc-icon-button.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring::after,.mdc-icon-button:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring::after{content:"";border:2px solid transparent;border-radius:8px;display:block;position:absolute;top:50%;left:50%;transform:translate(-50%, -50%);height:calc(100% + 4px);width:calc(100% + 4px)}}@media screen and (forced-colors: active)and (forced-colors: active){.mdc-icon-button.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring::after,.mdc-icon-button:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring::after{border-color:CanvasText}}.mdc-icon-button.mdc-icon-button--reduced-size .mdc-icon-button__ripple{width:40px;height:40px;margin-top:4px;margin-bottom:4px;margin-right:4px;margin-left:4px}.mdc-icon-button.mdc-icon-button--reduced-size.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring,.mdc-icon-button.mdc-icon-button--reduced-size:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring{max-height:40px;max-width:40px}.mdc-icon-button .mdc-icon-button__touch{position:absolute;top:50%;height:48px;left:50%;width:48px;transform:translate(-50%, -50%)}.mdc-icon-button:disabled{color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-disabled-on-light, rgba(0, 0, 0, 0.38))}.mdc-icon-button svg,.mdc-icon-button img{width:24px;height:24px}.mdc-icon-button{display:inline-block;position:relative;box-sizing:border-box;border:none;outline:none;background-color:transparent;fill:currentColor;color:inherit;text-decoration:none;cursor:pointer;user-select:none;z-index:0;overflow:visible}.mdc-icon-button .mdc-icon-button__touch{position:absolute;top:50%;height:48px;left:50%;width:48px;transform:translate(-50%, -50%)}.mdc-icon-button:disabled{cursor:default;pointer-events:none}.mdc-icon-button--display-flex{align-items:center;display:inline-flex;justify-content:center}.mdc-icon-button__icon{display:inline-block}.mdc-icon-button__icon.mdc-icon-button__icon--on{display:none}.mdc-icon-button--on .mdc-icon-button__icon{display:none}.mdc-icon-button--on .mdc-icon-button__icon.mdc-icon-button__icon--on{display:inline-block}.mdc-icon-button__link{height:100%;left:0;outline:none;position:absolute;top:0;width:100%}.mdc-icon-button{display:inline-block;position:relative;box-sizing:border-box;border:none;outline:none;background-color:transparent;fill:currentColor;color:inherit;text-decoration:none;cursor:pointer;user-select:none;z-index:0;overflow:visible}.mdc-icon-button .mdc-icon-button__touch{position:absolute;top:50%;height:48px;left:50%;width:48px;transform:translate(-50%, -50%)}.mdc-icon-button:disabled{cursor:default;pointer-events:none}.mdc-icon-button--display-flex{align-items:center;display:inline-flex;justify-content:center}.mdc-icon-button__icon{display:inline-block}.mdc-icon-button__icon.mdc-icon-button__icon--on{display:none}.mdc-icon-button--on .mdc-icon-button__icon{display:none}.mdc-icon-button--on .mdc-icon-button__icon.mdc-icon-button__icon--on{display:inline-block}.mdc-icon-button__link{height:100%;left:0;outline:none;position:absolute;top:0;width:100%}:host{display:inline-block;outline:none}:host([disabled]){pointer-events:none}.mdc-icon-button i,.mdc-icon-button svg,.mdc-icon-button img,.mdc-icon-button ::slotted(*){display:block}:host{--mdc-ripple-color: currentcolor;-webkit-tap-highlight-color:transparent}:host,.mdc-icon-button{vertical-align:top}.mdc-icon-button{width:var(--mdc-icon-button-size, 48px);height:var(--mdc-icon-button-size, 48px);padding:calc( (var(--mdc-icon-button-size, 48px) - var(--mdc-icon-size, 24px)) / 2 )}.mdc-icon-button i,.mdc-icon-button svg,.mdc-icon-button img,.mdc-icon-button ::slotted(*){display:block;width:var(--mdc-icon-size, 24px);height:var(--mdc-icon-size, 24px)}`;

/**
 * @license
 * Copyright 2018 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
/** @soyCompatible */
let IconButton = class IconButton extends IconButtonBase {
};
IconButton.styles = [styles$1];
IconButton = __decorate([
    e$7('mwc-icon-button')
], IconButton);

/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-LIcense-Identifier: Apache-2.0
 */
const styles = i$3 `:host{font-family:var(--mdc-icon-font, "Material Icons");font-weight:normal;font-style:normal;font-size:var(--mdc-icon-size, 24px);line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;-moz-osx-font-smoothing:grayscale;font-feature-settings:"liga"}`;

/**
 * @license
 * Copyright 2018 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
/** @soyCompatible */
let Icon = class Icon extends s {
    /** @soyTemplate */
    render() {
        return x `<span><slot></slot></span>`;
    }
};
Icon.styles = [styles];
Icon = __decorate([
    e$7('mwc-icon')
], Icon);

var badbad = "data:image/gif;base64,R0lGODlh9AH0AeZ/AESK/53C/4Kx/7bR/2Se//j7/8HY//r8/5G6/3Gm/0iM/97q/2Gc/87g//T4/67M/+Xu/26l//P3/+fw/+ry/06Q/6XH/6bI/4Wz/464/9Tk/16a/+70/1iX/5rA/1qY/3mr/7jS/77X/9ro/3So/4q2/6jJ/5S8/1SU/5i//6vK//D2/2ig/1CS/9Di/9Lj/+Ds/8re/1KT/9zp/7rU/7PP/9jn/4y3/6HE/6DE/2ui/3qs/8fc/2ag/4i1/+bv/8zf/9bl//3+/9zq/8bc/0aM/3eq/4e0/2yj/0yP/1aW/////0qO/36u/8Xa/0WK/0WL/6zL/0aL/1aV/02Q//7+/0uO/2Cb/+30/8Ta/3+v//z9/9fm/3yt/+Lt/7HO/0uP/8Xb//D1//f6/0+R/1OU//P4/7zV/1yZ/+vz/6PF/+Pu/12a/32u/3ap//X5/8bb/5e+/6DD/73W/5O8/5W9/7PQ/6/N/8nd//7//36v/3+u/0mN/9/r/2mh/////yH/C05FVFNDQVBFMi4wAwEAAAAh/wtYTVAgRGF0YVhNUDw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDkuMC1jMDAwIDc5LmRhNGE3ZTVlZiwgMjAyMi8xMS8yMi0xMzo1MDowNyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDozY2Y2NDdlNC02MGZkLTQxYmMtYWI3NC04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EypcyLChw4cQI0qcSLGixYsYM2rcyLGjx48gQ4ocSbKkyZMoU6pcybKly5cwY8qcSbOmzZs4c+rcybOnz59AgwodSrSo0aNIkypdyrSp06dQo0qdSrWq1atYs2rdyrWr169gw4odS7as2bNo06pdy7at27dw/+PKnUu3rt27ePPq3cu3r9+/gAMLHky4sOHDiBMrXsy4sePHkCNLnky5suXLmDNr3sy5s+fPoEOLHk26tOnTqFOrXs26tevXsGPLnk27tu3buHPr3s27t+/fwIMLH068uPHjyJMrX868ufPn0KNLn069uvXr2LNr3869u/fv4MOLH0++vPnz6NOrX8++vfv38OPLn0+/vv37+PPr38+/v///AAYo4IAEFmjggQgmqOCCDDbo4IMQRijhhBRWaOGFGGao4YYcdujhhyCGKOKIJJZo4okopqjiiiy26OKLMMYo44w01mjjjTjmqOOOPPbo449ABinkkEQWaeSRSCap5P+STDbp5JNQRinllFRWaeWVWGap5ZZcdunll2CGKeaYZJZp5plopqnmmmy26eabcMYp55x01mnnnXjmqeeefPbp55+ABirooIQWauihiCaq6KKMNuroo5BGKumklFZq6aWYZqrpppx26umnoIYq6qiklmrqqaimquqqrLbq6quwxirrrLTWauutuOaq66689urrr8AGK+ywxBZr7LHIJqvsssw26+yz0EYr7bTUVmvttdhmq+223Hbr7bfghivuuOSWa+656Kar7rrstuvuu/DGK++89NZr77345qvvvvz26++/AAcs8MAEF2zwwQgnrPDCDDfs8MMQRyzxxBRXbPEOxRhnrPHGHHfs8cfcBAIAIfkECQMAfwAsAAAAAPQB9AEAB/+Af4KDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbigJdO38mnKOkpaanqKmqq6ytrq+KMgCztAo9sLi5uru8vb6/wJlPtMSzUDfBycrLzM3Oz7g9xdMATdDX2Nna29y6stTF3eLj5OXm41PgxVPn7e7v8PGm0urE8vf4+fr49fb7/wADClyWpN+sMwMTKlzIkJQJgwAaSpxIseIheuqoWNzIsSPAFvUEeBxJsmQ5BuCsmFzJsqUzK8UquJxJs6YuEgwY1LHJs6fPn0CDCh1KtKjRo0iTKl3KtKnTp1CjSp1KtarVq1izanWqBQ0Z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";

var badmorph = "../static/bad-morph-c2bb8f615fe93323.gif";

var land$1 = "data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20data-name%3D%22Layer%202%22%20viewBox%3D%220%200%201287.15%2038.21%22%3E%3Cg%20data-name%3D%22Layer%202%22%3E%3Cpath%20d%3D%22M1015.47%2032.86V16.23h6.44v16.63%22%20style%3D%22fill%3A%231d3ba9%22%2F%3E%3Cpath%20d%3D%22M1011.69%2017.09s-4.06%203.8-6.43.02c-2.37-3.79%201.02-3.57%201.02-3.57s-1.61-3.51.42-5.8%203.64-1.27%203.64-1.27-.76-3.81.93-4.4%203.21%201.52%203.21%201.52.68-3.93%203.3-3.57%203.05%203.66%203.05%203.66%202.37-1.95%204.06-.17%201.18%204.48%201.18%204.48%201.61-3.14%203.89-2.25%201.52%203.09%201.52%203.09%202.37%201.5%201.1%203.03-3.64%202.39-3.64%202.39%203.3.79%202.45%202.67-3.81%201.85-3.81%201.85l-2.37%201.14h-8.12s-3.38%201.43-4.23.5-1.18-3.34-1.18-3.34Z%22%20style%3D%22fill%3A%234db6ac%22%2F%3E%3Cpath%20d%3D%22M0%2038.21V8.39c11.13%201.08%2065.43%2017.4%2086.67%2016.08s47.4%205.28%2054%207.49%2030.36-4.19%2053.46-11.1S313.6%2031.73%20343.3%2031.95s28.38-5.5%2043.56-8.34%2057.42%205.47%2079.86%206.02%2059.14-6.02%2059.14-6.02c19.73-3.77%2032.73-14.57%2048.01-12.14s28.59%205.33%2042.72%205.86%2045.82-3.34%2053.74-5.86%2035.64-5.4%2043.56%200%2018.15%202.39%2035.64%2014.17c7.45%205.02%2034.65%206.35%2042.57%207.54s64.02.3%2069.3-1.24%2034.72-6.47%2043.1-5.98%2092.86%204.88%20107.39%205.98%2066.66-2.03%2089.76-2.12%2046.2-.31%2059.4%202.12c10.51%201.93%2025.61-.92%2036.33-2.2%201.3-.16%202.53-.35%203.69-.39%2033.98-1.17%2041.27%207.55%2049%204.27s13.53-7.51%2037.04-9.16V38.2H0Z%22%20style%3D%22fill%3A%230c2b77%22%2F%3E%3C%2Fg%3E%3C%2Fsvg%3E";

var castle$1 = "../static/castle-alternate-7575ab637e5138e2.svg";

var demoCSS = i$3`
  /* Generic */
  ul.unstyled {
    padding: 0;
    margin: 0;
    list-style-type: none;
  }
  dl.unstyled,
  .unstyled dt,
  .unstyled dd {
    margin: 0;
    padding: 0;
  }
  p,
  h1,
  h2,
  h3,
  h4,
  h5,
  legend,
  pre {
    font: inherit;
    margin: 0;
    padding: 0;
  }
  p,
  span {
    font-family: var(--mono);
  }
  /* Variables */
  #demo {
    /* Blues */
    --blue-10: 217.2, 100%, 88.6%;
    --blue-20: 217.4, 100%, 75.5%;
    --blue-30: 217.5, 100%, 63.3%;
    --blue-40: 214.1, 81.7%, 50.6%;
    --blue-50: 211.3, 100%, 41.4%;
    --blue-60: 214.4, 98%, 38.4%;
    /* Grays */
    --gray-10: 0, 0%, 93.7%;
    --gray-20: 0, 0%, 86.7%;
    --gray-30: 0, 0%, 74.9%;
    --gray-40: 207.3, 4.5%, 52.4%;
    --gray-50: 200, 4.3%, 41%;
    --gray-60: 204, 3.8%, 25.7%;
    /* Indigos */
    --indigo-60: 227.1, 70.7%, 38.8%;
    --indigo-70: 222.6, 81.7%, 25.7%;
    --indigo-80: 225.3, 76%, 14.7%;
    /* Purples */
    --purple-30: 266, 69%, 63.3%;
    --purple-40: 272.1, 62.3%, 40.6%;
    --purple-50: 269.2, 75.2%, 28.4%;
    /* Pinks */
    --pink-20: 321.6, 100%, 77.6%;
    --pink-30: 327.4, 83.3%, 62.4%;
    --pink-40: 323.9, 98.3%, 47.1%;
    --pink-50: 321.3, 92%, 39%;
    /* Greens */
    --green-20: 174.7, 41.3%, 78.6%;
    --green-30: 172.4, 51.9%, 58.4%;
    --green-40: 174.3, 41.8%, 50.8%;
    --green-50: 172.7, 60.2%, 37.5%;
    /* Custom Colors */
    --drawer-ditch: 230, 14%, 17%;
    --drawer-glow: hsl(227, 63%, 14%, 15%);
    --drawer-highlight: 240, 52%, 11%;
    --drawer-lowlight: 240, 52%, 1%;
    --drawer-surface: 240, 52%, 6%;
    --content-glow: 235, 69%, 18%;
    --content-gloam: 235, 69%, 18%;
    --content-surface: 227, 63%, 9%;
    --highlight-text: white;
    --lowlight-text: 218, 27%, 68%;
    --link-normal: 221, 92%, 71%;
    --link-focus: 221, 92%, 100%;
    /* Sizes */
    --bar-height-flex: var(--bar-height-short);
    --bar-height-short: 4.68rem;
    --bar-height-tall: 8.74rem;
    --bottom-castle: 24vh;
    --bottom-land: 10vh;
    --button-corners: 3.125rem;
    --content-width: calc(100vw - var(--drawer-width));
    --drawer-width-collapsed: 40px;
    --drawer-width: calc(var(--line-length-short) + var(--size-xhuge));
    --example-width: min(var(--line-length-wide), var(--content-width));
    --field-width: calc(var(--example-width) * 0.74);
    --line-length-short: 28rem;
    --line-length-wide: 40rem;
    --line-short: 1.4em;
    --line-tall: 1.8em;
    --size-colassal: 4rem;
    --size-gigantic: 5rem;
    --size-huge: 2rem;
    --size-jumbo: 3rem;
    --size-large-em: 1.26em;
    --size-large: 1.26rem;
    --size-micro: 0.28rem;
    --size-mini: 0.6rem;
    --size-normal: 1rem;
    --size-small: 0.8rem;
    --size-xgigantic: 6.26rem;
    --size-xhuge: 2.6rem;
    --size-xlarge: 1.66rem;
    /* Timings */
    --drawer-lapse: 100ms;
    --full-lapse: 300ms;
    --half-lapse: 150ms;
    --quick-lapse: 50ms;
    /* Fonts */
    --title: "Press Start 2P", sans-serif;
    --mono: "Roboto Mono", monospace;
    --sans-serif: "Roboto", sans-serif;
  }
  /* Links */
  a {
    color: hsl(var(--link-normal));
    text-decoration: none;
    vertical-align: bottom;
  }
  #guide a {
    font-weight: normal;
    text-decoration: underline;
    color: hsl(var(--lowlight-text));
  }
    color: hsl(var(--lowlight-text));
  }
  #guide a:focus mwc-icon,
  #guide a:hover mwc-icon,
  #guide a:hover,
  #guide a:focus,
  #guide a:active,
  #guide a:active mwc-icon a span {
    color: hsl(var(--link-focus));
  }
  a mwc-icon {
    --mdc-icon-size: var(--size-large-em);
    bottom: -4px; /* TODO: magic numbers */
    color: hsl(var(--link-focus));
    position: relative;
  }
  a,
  a span,
  a mwc-icon {
    transition: color var(--half-lapse) ease-out 0s,
      text-decoration var(--half-lapse) ease-out 0s,
      transform var(--half-lapse) ease-out 0s;
  }
  a span + mwc-icon,
  a mwc-icon + span {
    margin-left: var(--size-micro);
  }
  a:focus mwc-icon,
  a:hover mwc-icon,
  a:active mwc-icon {
    transform: scale(1.1);
  }
  a:focus,
  a:hover,
  a:active {
    color: hsl(var(--link-focus));
  }
  a:focus mwc-icon,
  a:hover mwc-icon,
  a:active mwc-con {
    color: hsl(var(--link-normal));
  }
  #sitemap a:focus,
  #sitemap a:hover,
  #sitemap a:active {
    color: var(--highlight-text);
  }
  #guide a:focus span,
  #guide a:hover span,
  #guide a:active span,
  #sitemap a:focus,
  #sitemap a:hover,
  #sitemap a:active {
    text-decoration: hsl(var(--link-focus)) dotted underline 1px;
    text-underline-offset: 2px;
  }
  /* Demo */
  :host {
    display: block;
  }
  :host,
  #demo {
    font-family: var(--sans-serif);
    font-size: var(--size-normal);
    height: 100%;
    min-height: 100vh;
    max-width: 100%;
    width: 100%;
    background-color: hsl(var(--drawer-surface));
  }
  #demo {
    color: var(--highlight-text);
    display: grid;
    grid-template-columns: var(--drawer-width) 1fr;
    grid-template-rows: 1fr;
    transition: grid-template-columns var(--drawer-lapse) ease-out 0s;
  }
  #demo.drawerClosed {
    /* TODO: redo for new drawer-peek layout, share variables */
    grid-template-columns: var(--drawer-width-collapsed) 1fr;
  }
  #demo.game {
    visibility: hidden;
  }
  #drawer {
    background: linear-gradient(
          to left,
          hsl(var(--drawer-ditch)) 1px,
          transparent 1px
        )
        0 0 / var(--drawer-width) 100vh no-repeat fixed,
      radial-gradient(
          ellipse at left,
          hsl(var(--drawer-lowlight), 70%) -10%,
          transparent 69%
        )
        calc((100vw - (var(--drawer-width) / 2)) * -1) -150vh / 100vw 400vh no-repeat
        fixed,
      radial-gradient(
          ellipse at right,
          hsl(var(--drawer-highlight), 70%) -10%,
          transparent 69%
        )
        calc(var(--drawer-width) / 2) -150vh / 100vw 400vh no-repeat fixed,
      linear-gradient(
          to right,
          hsl(var(--drawer-lowlight), 20%) 0,
          transparent 50%
        )
        0 0 / var(--drawer-width) 100vh no-repeat fixed,
      linear-gradient(
          to bottom,
          hsl(var(--drawer-lowlight), 30%) 0,
          transparent 50%
        )
        0 0 / var(--drawer-width) 100vh no-repeat fixed,
      linear-gradient(
          to left,
          hsl(var(--drawer-highlight), 10%) 0,
          transparent 25%
        )
        0 0 / var(--drawer-width) 100vh no-repeat fixed,
      linear-gradient(
          to top,
          hsl(var(--drawer-highlight), 10%) 0,
          transparent 50%
        )
        0 0 / var(--drawer-width) 100vh no-repeat fixed,
      linear-gradient(
          to right,
          hsl(var(--drawer-lowlight), 80%) 2px,
          transparent 2px
        )
        0 0 / var(--drawer-width) 100vh no-repeat fixed,
      linear-gradient(
          to bottom,
          hsl(var(--drawer-lowlight), 80%) 2px,
          transparent 2px
        )
        0 0 / var(--drawer-width) 100vh no-repeat fixed,
      linear-gradient(
          to left,
          hsl(var(--drawer-highlight), 80%) 1px,
          transparent 1px
        )
        0 0 / var(--drawer-width) 100vh no-repeat fixed,
      linear-gradient(
          to top,
          hsl(var(--drawer-highlight), 80%) 1px,
          transparent 1px
        )
        0 0 / var(--drawer-width) 100vh no-repeat fixed,
      hsl(var(--drawer-surface));
    border-right: 2px solid hsl(var(--drawer-ditch));
    box-shadow: 5px 0 9px 0 var(--drawer-glow);
    padding-bottom: 60px; /* TODO: offset for disclaimer */
    position: relative;
    z-index: 20;
  }
  #drawer > .drawerIcon {
    /* TODO: redo for new drawer-peek layout, share variables */
    --mdc-icon-size: var(--size-xlarge);
    inset: auto 0 auto auto;
    position: absolute;
    transition: opacity var(--half-lapse) ease-out 0s;
    z-index: 4;
    transform: translateX(50%) translateY(50vh);
    border: 2px solid #252731;
    background-color: hsl(var(--drawer-surface));
    border-radius: 40px;
    transition: 200ms ease-in-out;
  }
  .drawerOpen #drawer > .drawerIcon {
    transform: none;
    border: none;
    background: none;
  }
  #drawer > .drawerIcon[disabled] {
    --mdc-theme-text-disabled-on-light: hsl(var(--gray-40));
    opacity: 0.74;
  }
  .drawerClosed #drawer > .drawerCloseIcon {
    opacity: 0;
    transition-delay: 0;
  }
  .drawerOpen #drawer > .drawerCloseIcon {
    opacity: 1;
    transition-delay: var(--half-lapse);
  }

  #drawer .disclaimer {
    bottom: 0;
    color: hsla(var(--lowlight-text), 0.8);
    display: block;
    font-size: 0.6em; /* TODO: variable, font size accessibility */
    font-style: italic; /* TODO: dyslexia */
    font-weight: 100;
    line-height: 1.25; /* TODO: variable */
    padding: var(--size-xhuge);
    position: absolute;
    visibility: hidden;
    transition: none;
    opacity: 0;
  }
  .drawerOpen #drawer .disclaimer {
    visibility: visible;
    transition: 1000ms opacity;
    opacity: 1;
  }
  /* Content */
  #content {
    font-family: var(--mono);
    /* This transform may be required due to paint issues with animated elements in drawer
     However, using this also prevents background-attachment: fixed from functioning
     Therefore, background has to be moved to internal wrapper .sticky */
    /* transform: translateZ(0); */
  }
  #content .sticky {
    /* Due to CSS grid and sticky restrictions, have to add internal wrapper
     to get sticky behavior, centering in viewport behavior, and fixed background */
    position: sticky;
    top: 0;
  }
  .animating #content .sticky {
    overflow-y: hidden;
  }
  #content .relative {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr;
    justify-content: safe center;
    position: relative;
  }
  #content .sticky,
  #content .relative {
    min-height: 100vh;
  }
  .drawerOpen #content .sticky {
    --offset: calc(50% + (var(--drawer-width) / 2));
    background-position:
    /* castle */ var(--offset) var(--content-bottom),
      /* land */ var(--offset) var(--land-content-bottom),
      /* pink */ var(--offset) 75vh, /* purple */ var(--offset) 50vh,
      /* blue */ var(--offset) var(--bar-height-short);
  }
  #content .sticky {
    --content-bottom: calc(100vh - var(--bottom-castle));
    --land-content-bottom: calc(100vh - var(--bottom-land));
    background: 
    /* castle */ url(${r$2(castle$1)}) center
        var(--content-bottom) / auto var(--bottom-castle) no-repeat fixed,
      /* land */ url(${r$2(land$1)}) center var(--land-content-bottom) /
        auto var(--bottom-land) no-repeat fixed,
      /* pink */
        radial-gradient(
          ellipse at bottom,
          hsl(var(--pink-40), 64%) 0,
          transparent 69%
        )
        center 75vh / 80vw 100vh no-repeat fixed,
      /* purple */
        radial-gradient(
          ellipse at bottom,
          hsl(var(--purple-30), 64%) 0,
          transparent 69%
        )
        center 50vh / 200vw 100vh no-repeat fixed,
      /* blue */
        radial-gradient(
          circle,
          hsl(var(--content-gloam), 56%) -20%,
          transparent 50%
        )
        center var(--bar-height-short) / 68vw 68vh no-repeat fixed,
      /* color */ hsl(var(--content-surface));
    transition: background-position var(--drawer-lapse) ease-out 0s;
  }
  /* Sitemap */
  #sitemap {
    /* TODO: redo for new drawer-peek layout, share variables */
    --map-bg-width: 240vw;
    --map-bg-height: 62vh;
    --map-bg-offset: 52vh;
    align-content: center;
    align-items: center;
    /* TODO: redo for new drawer-peek layout, share variables */
    background: 
      /* gradient */ radial-gradient(
          ellipse at bottom,
          hsl(0, 0%, 0%, 15%) 5%,
          hsl(var(--content-surface)) 58%
        )
        center var(--map-bg-offset) / var(--map-bg-width) var(--map-bg-height)
        no-repeat fixed,
      /* color */ hsl(var(--content-surface));
    box-sizing: border-box;
    display: grid;
    grid-template-columns: auto;
    grid-template-rows: auto auto auto;
    font-family: var(--mono);
    justify-content: center;
    inset: var(--bar-height-flex) 0 0 0;
    margin-left: 0;
    padding: var(--size-huge);
    position: absolute;
    transition: transform var(--full-lapse) ease-out 0s,
      background-position var(--drawer-lapse) ease-out 0s,
      background-size var(--drawer-lapse) ease-out 0s,
      margin-left var(--drawer-lapse) ease-out 0s,
      padding-left var(--drawer-lapse) ease-out 0s;
    z-index: 10;
  }
  #sitemap .fade {
    margin: auto;
    max-width: var(--content-width);
    width: var(--example-width);
    transition: opacity var(--full-lapse) ease-in 0s;
  }
  .sitemapOpen #sitemap {
    transform: translateY(0);
  }
  .sitemapOpen #sitemap .fade {
    opacity: 1;
    transition-delay: var(--half-lapse);
  }
  .sitemapClosed #sitemap {
    transform: translateY(100%);
    pointer-events: none;
  }
  .sitemapClosed #sitemap .fade {
    opacity: 0;
  }
  .drawerOpen #sitemap {
    --stack-size: calc(var(--drawer-width) + var(--size-huge));
    /* TODO: redo for new drawer-peek layout, share variables */
    background-position: calc(50% + (var(--stack-size) / 2))
      var(--map-bg-offset);
    background-size: calc(var(--map-bg-width) - var(--stack-size))
      var(--map-bg-height);
    margin-left: calc(var(--drawer-width) * -1);
    padding-left: var(--stack-size);
  }
  #demo:not(.animating).sitemapClosed #sitemap {
    max-height: 0;
    max-width: 0;
    opacity: 0;
    z-index: -2;
  }
  #sitemap .links {
    display: grid;
    font-family: var(--title);
    gap: var(--size-huge);
    grid-template-areas: "game home signup" "game comments store" "game login .";
    grid-template-columns: 1fr 1fr 1fr;
    grid-template-rows: auto auto auto;
    margin-bottom: var(--size-gigantic);
    white-space: nowrap;
  }
  /* TODO: redo for new drawer-peek layout, updated queries
@media screen and (max-width: 32.8125em), screen and (max-width: 28.125em) {
  #sitemap .links {
    grid-template-areas: "game home" "login signup" "comments store";
    grid-template-columns: auto auto;
    grid-template-rows: auto auto auto;
    margin-bottom: var(--size-jumbo);
  }
}
@media screen and (max-width: 21.875em) {
  #sitemap .links {
    grid-template-areas: "game" "home" "signup" "login" "store" "comments";
    grid-template-columns: auto;
    grid-template-rows: auto auto auto auto auto auto;
    margin-bottom: var(--size-huge);
  }
}
*/
  #sitemap .h1,
  #sitemap p {
    line-height: var(--line-tall);
  }
  #sitemap .h1 {
    color: var(--highlight-text);
    font-size: var(--size-large);
    font-weight: bold;
    margin-bottom: var(--size-small);
  }
  #sitemap p {
    color: hsl(var(--lowlight-text));
    margin-bottom: var(--size-normal);
  }
  #sitemap .game {
    grid-area: game;
    /* TODO: ??? white-space: break-spaces; */
  }
  #sitemap .home {
    grid-area: home;
  }
  #sitemap .comments {
    grid-area: comments;
  }
  #sitemap .login {
    grid-area: login;
  }
  #sitemap .signup {
    grid-area: signup;
  }
  #sitemap .store {
    grid-area: store;
  }
  /* Bar */
  #bar {
    align-items: end;
    background: hsl(var(--content-surface));
    display: grid;
    gap: 0 var(--size-small);
    grid-template-areas: "h1 sitemapIcon" "h2 sitemapIcon";
    grid-template-columns: max-content auto;
    grid-template-rows: auto auto;
    justify-content: stretch;
    margin: 0 0 var(--size-huge) 0;
    padding: var(--size-small);
    position: sticky;
    top: 0;
    z-index: 30;
  }
  #bar .h1 {
    font-family: "Press Start 2P", monospace;
    font-size: var(--size-large);
    grid-area: h1;
  }
  #bar .h2 {
    color: hsl(var(--gray-40));
    font-size: var(--size-normal);
    grid-area: h2;
  }
  #bar .h2 abbr {
    text-decoration: none;
  }
  #bar .sitemapIcon {
    --mdc-icon-size: var(--size-xlarge);
    grid-area: sitemapIcon;
    justify-self: right;
  }
  /* Example */
  #example {
    box-sizing: border-box;
    margin: auto;
    max-width: var(--content-width);
    width: var(--example-width);
    padding: var(--size-jumbo) var(--size-jumbo)
      calc(var(--bottom-castle) * 0.75) var(--size-jumbo);
  }
  #example fieldset {
    margin-bottom: var(--size-jumbo);
    position: relative;
    z-index: 2;
  }
  #example .fields {
    margin: 0 auto;
    max-width: var(--content-width);
    width: var(--field-width);
  }
  #example .h3 {
    color: var(--highlight-text);
    font-family: var(--title);
    font-size: var(--size-xlarge);
    letter-spacing: 2px;
    line-height: var(--size-large-em);
    margin-bottom: var(--size-normal);
    text-transform: capitalize;
  }
  #example.home .h3 {
    font-size: var(--size-huge);
    text-transform: none;
  }
  #example .h3 {
    text-shadow: -2px -2px 0 hsl(var(--content-gloam)),
      2px 2px 0 hsl(var(--content-surface)),
      -2px 2px 0 hsl(var(--content-surface)),
      2px -2px 0 hsl(var(--content-surface));
  }
  #example p {
    color: hsl(var(--lowlight-text));
    line-height: var(--line-tall);
    margin-bottom: var(--size-huge);
    text-shadow: -1px -1px 0 hsl(var(--content-surface)),
      1px 1px 0 hsl(var(--content-surface)),
      -1px 1px 0 hsl(var(--content-surface)),
      1px -1px 0 hsl(var(--content-surface));
  }
  #example p:last-of-type {
    --negative-size: calc(var(--size-colassal) * -1);
    background: linear-gradient(
          90deg,
          transparent 0%,
          hsl(var(--content-gloam)) 15%,
          hsl(var(--content-gloam)) 30%,
          hsl(var(--content-glow)) 50%,
          hsl(var(--content-gloam)) 70%,
          hsl(var(--content-gloam)) 85%,
          transparent 100%
        )
        center bottom / 100% 1px no-repeat scroll,
      radial-gradient(
          ellipse at bottom,
          hsl(var(--content-gloam), 36%),
          transparent 70%
        )
        center bottom / 100% 50% no-repeat scroll,
      transparent;
    margin: 0 var(--negative-size) var(--size-jumbo) var(--negative-size);
    padding: 0 var(--size-colassal) var(--size-large);
  }
  #example.home p:last-of-type {
    background: none;
    border: 0;
    margin-bottom: var(--size-jumbo);
    padding-bottom: 0;
  }
  /* Form */
  fieldset {
    border: 0;
    display: block;
    margin: 0;
    padding: 0;
  }
  legend {
    display: block;
    font: inherit;
    margin: 0;
    padding: 0;
    width: 100%;
  }
  label {
    display: block;
  }
  label {
    font-weight: bold;
    letter-spacing: 0.5px;
    line-height: 1;
  }
  label:not(:last-child) {
    margin-bottom: var(--size-xlarge);
  }
  label > span {
    display: block;
    margin-bottom: var(--size-small);
  }
  input,
  textarea {
    background: hsl(var(--gray-60));
    border: 0 solid transparent;
    border-radius: 2px;
    box-sizing: border-box;
    color: inherit;
    display: block;
    font-family: var(--sans-serif);
    line-height: 1;
    margin: 0;
    padding: var(--size-small);
    width: 100%;
  }
  textarea {
    line-height: var(--line-short);
    min-height: calc(var(--line-short) * 6);
  }
  /* Guide */
  #guide {
    color: hsl(var(--lowlight-text));
    overflow: hidden;
    transform: translateZ(0);
    width: 100%;
    font-size: var(--size-small);
  }
  .mask {
    transition: opacity var(--half-lapse) ease-out 0s;
    width: var(--drawer-width);
  }
  .drawerOpen .mask {
    opacity: 1;
  }
  .drawerClosed .mask {
    opacity: 0;
  }
  #guide .h1,
  #guide .h2 {
    color: var(--highlight-text);
    font-size: var(--size-large);
    font-weight: bold;
  }
  #guide .h1 {
    border: 0 solid hsl(var(--drawer-ditch));
    border-width: 2px 0;
    font-size: var(--size-md);
    letter-spacing: 3px;
    line-height: 1;
    padding: var(--size-small);
    text-transform: uppercase;
  }
  #guide .text:first-child .h1 {
    border-top-color: transparent;
  }
  #guide .h2 {
    line-height: var(--size-large-em);
    margin-bottom: var(--size-mini);
  }
  #guide p {
    color: hsl(var(--lowlight-text));
    line-height: var(--line-short);
    max-width: var(--line-length-short);
  }
  #guide a,
  #guide code,
  #guide pre {
    display: block;
  }
  #guide .h1,
  #guide .text.result {
    margin-bottom: var(--size-huge);
  }
  #guide .text,
  #guide #verdict + .scoreExample {
    margin-bottom: var(--size-xhuge);
  }
  #guide p,
  #guide .code {
    margin-bottom: var(--size-normal);
  }
  #guide .h2,
  #guide p,
  #guide a.documentation {
    padding: 0 var(--size-xhuge);
  }
  #guide .code {
    /* TODO: code block background color */
    color: var(--highlight-text);
    background: hsl(0, 0%, 100%, 5%);
    margin: 0 var(--size-xhuge) var(--size-xhuge);
    padding: var(--size-small) var(--size-normal);
    margin-bottom: var(--size-large);
    position: relative;
  }
  #guide a.log {
    padding: var(--size-small) var(--size-huge);
  }
  #guide a.log.disabled {
    display: none;
  }
  /* Guide Score */
  #score {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: var(--size-huge);
    margin: 0 var(--size-gigantic) var(--line-short);
    padding-top: var(--size-micro);
    padding-bottom: var(--size-xhuge);
  }
  #score p {
    margin-bottom: 0;
    padding: 0 var(--size-small);
  }
  #score .score {
    display: flex;
    flex-direction: column;
    gap: var(--size-small);
    line-height: 1;
  }
  .score {
    color: hsl(var(--link-normal));
    font-family: var(--sans-serif);
    font-size: var(--size-jumbo);
    font-weight: bold;
    line-height: 1;
    text-indent: -0.1em;
  }
  #score img {
    height: calc(var(--size-jumbo) * 1.35);
    width: auto;
  }
  /* Store Cart */
  dl.cart {
    --stoplight-accent: 13px;
    margin-bottom: var(--size-jumbo);
  }
  .cart .item {
    display: flex;
    align-items: top;
    justify-content: space-between;
    margin-bottom: var(--size-xlarge);
  }
  .cart img {
    height: auto;
    width: 50px;
  }
  .cart .stoplight img {
    margin-top: calc(var(--stoplight-accent) * -1);
  }
  .cart dt {
    flex: 0 0 var(--size-gigantic);
    margin-right: var(--size-xlarge);
    padding-top: var(--stoplight-accent);
  }
  .cart dd:not(:last-child) {
    flex: 1 0 auto;
    margin-top: calc(
      var(--size-normal) + var(--stoplight-accent) + var(--size-small)
    );
  }
  .cart dd:last-child {
    flex: 0 0 var(--size-gigantic);
  }
  /* Guide Animation */
  @keyframes scoreBump {
    from {
      transform: scale(1) translate(0, 0);
    }
    to {
      transform: scale(1.14) translate(-2%, 0);
    }
  }
   @keyframes drawerBump {
    70% { transform:translateX(0%); }
    80% { transform:translateX(17%); }
    90% { transform:translateX(0%); }
    95% { transform:translateX(8%); }
    97% { transform:translateX(0%); }
    99% { transform:translateX(3%); }
    100% { transform:translateX(0); }
  }
  #score {
    animation: var(--full-lapse) ease-out 0s 2 alternate both running scoreBump;
    transform-origin: left center;
  }
  .unscored #score, .draweropen.scored:not(.drawerClosed) {
    animation-play-state: paused;
  }

  .scored #score, .drawerClosed.scored #drawer,  .drawerClosed.scored:not(.drawerOpen)  {
    animation-play-state: running;
  }

 #drawer {
    animation:  .5s ease-out 0s 2 alternate both paused drawerBump;
  }
  #guide .response,
  #verdict p,
  .scoreExample {
    transition: max-height var(--full-lapse) ease-out var(--half-lapse),
      opacity var(--full-lapse) ease-out var(--half-lapse);
  }
  .unscored #guide .response,
  .unscored .scoreExample {
    max-height: 0;
    opacity: 0;
  }
  .scored #guide .response,
  .scored #verdict p,
  .scored .scoreExample {
    opacity: 1;
  }
  /* Slotted Checkbox */
  ::slotted(div.g-recaptcha) {
    display: flex;
    justify-content: center;
    margin: 0 auto var(--size-xhuge);
    position: relative;
    z-index: 1;
  }
  /* Slotted Button / Button */
  .button {
    margin-bottom: var(--size-jumbo);
  }
  ::slotted(button),
  .button {
    appearance: none;
    background: transparent /* hsl(var(--blue-50)) */;
    border: 0;
    border-radius: 0;
    color: var(--highlight-text);
    cursor: pointer;
    display: inline-block;
    font-family: var(--title);
    font-size: var(--size-small);
    line-height: var(--size-large-em);
    margin: 0 auto var(--size-xlarge);
    outline: 0;
    padding: var(--size-normal) var(--size-huge);
    position: relative;
    text-transform: uppercase;
    width: 100%;
    z-index: 0;
  }
  .button {
    width: auto;
  }
  /* Button Animation */
  ::slotted(button),
  .button,
  ::slotted(button)::after,
  .button::after,
  ::slotted(button)::before,
  .button::before {
    /* TODO: timing variables? */
    transition: border 50ms ease-out 0s, border-radius 50ms ease-out 0s,
      background 100ms ease-in-out 50ms, box-shadow 150ms ease-out 50ms,
      outline 50ms ease-out 0s, text-shadow 50ms ease-out 0s;
  }
  /* Button Layers */
  ::slotted(button)::after,
  .button::after,
  ::slotted(button)::before,
  .button::before {
    content: "";
    display: block;
    position: absolute;
    z-index: -1;
  }
  /* Button Text */
  ::slotted(button),
  .button {
    text-shadow: 2px 2px black;
  }
  /*
::slotted(button:focus),
.button:focus,
::slotted(button:hover),
.button:hover,
::slotted(button:active),
.button:active {
  text-shadow: black 2px 2px, hsl(var(--gray-50)) 4px 4px;
}

*/
  /* Button Shape */
  ::slotted(button)::before,
  .button::before {
    /* Round Glow Shape */
    border-radius: 100%;
    inset: 0 25%;
  }
  ::slotted(button),
  .button,
  ::slotted(button)::after,
  .button::after {
    /* Normal Shape */
    border-radius: 1px;
  }
  ::slotted(button:focus),
  .button:focus,
  ::slotted(button:focus)::after,
  .button:focus::after,
  ::slotted(button:focus-visible),
  .button:focus-visible,
  ::slotted(button:focus-visible)::after,
  .button:focus-visible::after,
  ::slotted(button:hover),
  .button:hover,
  ::slotted(button:hover)::after,
  .button:hover::after,
  ::slotted(button:active),
  .button:active,
  ::slotted(button:active)::after,
  .button:active::after {
    /* Focus/Hover/Active Shape */
    border-radius: var(--button-corners);
  }
  /* Button Background */
  ::slotted(button)::after,
  .button::after {
    /* background: hsl(var(--blue-40)); */
    background: hsl(var(--pink-40));
    inset: 0;
  }
  ::slotted(button:active)::after,
  .button:active::after {
    /* background: hsl(var(--blue-50)); */
    background: hsl(var(--pink-50));
  }
  /* Button Border */
  ::slotted(button)::after,
  .button::after {
    border: 1px solid transparent;
  }
  ::slotted(button:focus)::after,
  .button:focus::after,
  ::slotted(button:hover)::after,
  .button:hover::after {
    /* Focus/Hover Border */
    border-bottom: 1px solid rgba(0, 0, 0, 30%);
    border-right: 1px solid rgba(0, 0, 0, 30%);
    border-top: 1px solid rgba(255, 255, 255, 20%);
    border-left: 1px solid rgba(255, 255, 255, 20%);
  }
  ::slotted(button:active)::after,
  .button:active::after {
    /* Active Border */
    border-bottom: 1px solid rgba(255, 255, 255, 20%);
    border-right: 1px solid rgba(255, 255, 255, 20%);
    border-top: 1px solid rgba(0, 0, 0, 30%);
    border-left: 1px solid rgba(0, 0, 0, 30%);
  }
  ::slotted(button:focus-visible)::after,
  .button:focus-visible::after {
    /* Focus Outline */
    /* outline: 2px solid hsl(var(--blue-30)); */
    outline: 2px solid hsl(var(--pink-30));
    outline-offset: 4px;
  }
  ::slotted(button:hover)::after,
  .button:hover::after,
  ::slotted(button:active)::after,
  .button:active::after {
    outline: none;
  }
  /* Button Shadow */
  ::slotted(button:focus)::after,
  .button:focus::after,
  ::slotted(button:hover)::after,
  .button:hover::after {
    /* Focus/Hover Square Glow */
    box-shadow: 1px 2px var(--size-jumbo) 2px hsl(var(--blue-50), 32%);
  }
  ::slotted(button:active)::after,
  .button:active::after {
    /* Active Square Glow */
    box-shadow: 1px 2px var(--size-jumbo) 2px hsl(0, 0%, 0%, 10%);
  }
  ::slotted(button:focus)::before,
  .button:focus::before,
  ::slotted(button:hover)::before,
  .button:hover::before {
    /* Focus/Hover Round Glow */
    box-shadow: 2px 2px var(--size-xgigantic) 20px hsl(var(--blue-50), 32%);
  }
  ::slotted(button:active)::before,
  .button:active::before {
    /* Active Round Glow */
    box-shadow: 2px 2px var(--size-xgigantic) 20px hsl(0, 0%, 0%, 10%);
  }
`;

var human = "data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2049.58%2052.28%22%3E%3Cpath%20d%3D%22M35.73%2019.14c0-7.23-4.9-13.09-10.94-13.09s-10.94%205.86-10.94%2013.09c0%204.85%202.2%209.08%205.48%2011.34l.99%207.29s3.14%207.01%204.48%206.99c1.37-.02%204.51-7.22%204.51-7.22l.96-7.05c3.27-2.26%205.47-6.49%205.47-11.34Z%22%20style%3D%22fill%3A%2382b1ff%3Bopacity%3A.98%22%2F%3E%3Cpath%20d%3D%22M45.7%2024.85s-4.55-7.24-5.23-9.94C38.48%206.9%2033.45%200%2024.79%200c-.23%200-.46%200-.68.02-.2%200-.39.02-.58.04h-.05C15.62.72%2010.99%207.31%209.1%2014.91c-.67%202.7-5.23%209.94-5.23%209.94%202.22%204.21%207.42%208.42%2015.98%209.6l-.54-3.97c-3.1-2.15-5.24-6.06-5.46-10.6.37-10.43%2015.92-6.25%2017.76-10.96%202.5%202.4%204.1%206.08%204.1%2010.22%200%204.85-2.2%209.07-5.47%2011.34l-.54%203.97c8.56-1.18%2013.76-5.39%2015.98-9.6Z%22%20style%3D%22fill%3A%230c2b77%22%2F%3E%3Cpath%20d%3D%22m49.58%2052.28-6.45-11.49-7.37-1.35-6.21-3.75-.25%201.85s-3.14%207.2-4.51%207.22c-1.33.02-4.48-6.99-4.48-6.99l-.28-2.08-6.21%203.75-7.37%201.35L0%2052.28%22%20style%3D%22fill%3A%231a73e8%22%2F%3E%3C%2Fsvg%3E";

var hydrant$1 = "data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2059.7%2059.7%22%3E%3Cpath%20fill%3D%22%23448aff%22%20d%3D%22M.6.3h58.5v58.5H.6z%22%2F%3E%3Cg%20fill%3D%22%231a73e8%22%3E%3Cpath%20d%3D%22M30%206.4c.3%200%20.5%200%20.6-.2l.2-.3h.4l-.2-.4c.2%200%20.3.4.7%200l-.5-.8c-.1-.3-.3-.5-.3-.8s-.1-.5-.4-.6c-.3%200-.7-.1-.9.3l.5.6c0%20.3-.3.3-.5.4l-.1-.2c-.3%200-.4.2-.5.4V5h-.1l-.2.7-.7-.5c0-.3-.1-.5-.4-.5h-.4v.5l-.4.7c.5.4.8%201%201.6%201l.4-.6.5.2-.2.1c0%20.4.1.6.5.8.2-.3.5-.5.4-.9zm-4.3-4.9c.3%200%20.6-.1.8-.4L27%201h.3-2.6l.4.5c.2.2.4%200%20.7%200zM27%202.8l1.3.7c.5.2.7-.4%201.3-.3l-1-1H28l-.8.2c0-.4.4-.5.4-.8-.4-.2-.8-.3-1.2%200%200%20.2-.3.2-.4.3.3.8.5%201%201.2%201zm-5%203.8c.2%200%20.4%200%20.5-.3l.1-.2H24V4.7h-.6l-.4-.4-.8%201.5H22l-.3.4c0%20.2.2.3.4.4zm7%202.5c-.4%200-.8-.2-.9-.8%200-.3-.2-.5-.6-.4%200%20.1-.1.3%200%20.4l-.4.2c0%20.3.1.5.4.7l.3-.4.1.1v.6l.4.2-.2.7c.8.3.8.3%201.4-.4l-.3-.2-.3-.2.7-.3L29%209zM16%204.9c.5-.2.8-.5.7-1-.2-.5-.1-1-.2-1.5-.6-.2-.6.3-.8.6l.6.3c-.5.4-.8%201-.4%201.6zm21.8%2016.9.5-.4h-.4l.1-.6c0-.2-.1-.3-.3-.3l-.1-.4-.7-.4c-.3.3-.2.6-.1.8l.5.2v.6h-.1v.7h-.6c0%20.5.3.8.8%201%20.4-.3%200-.5%200-.9.2%200%20.3-.2.4-.3zm-7.8-6c.2-.2.2-.5.1-1-1.2.2-1.4.4-1%201.3.4.2.7%200%201-.3zm.8%203.2c.4-.2%200-.7.3-1-1.3.1-1.4.3-1.1%201.3.3.1.6%200%20.8-.2zM21.4%207.5l.4-.4h-.4c0-.5-.2-.9-.3-1.3l-.6-.3c-.4.2-.2.5-.2.8l.8.2-.3.6.5.5zm3.3-4.7.2.4.1-.3h.3v-.7c-.8-.6-.6-.6-1.3-.3%200%20.7.1.8.7%201zM21%204.4l1.1-1.2c0-.4-.4-.4-.7-.5-.7.8-.8%201-.3%201.7zm-5.9%202.9c.8-.5.8-1%200-1.4-.7.8-.6%201%200%201.4zm5.5-4%20.2-.6h-.6c-.2-.3%200-.7-.5-.6v1.3l.9-.1z%22%2F%3E%3Cpath%20d%3D%22M29.2%201.4c0-.3-.2-.4-.6-.4-.3%200-.6.3-.4.7%200%20.2.3.4.5.6.5-.3.6-.5.5-.9zM54.6%2026zM26.9%203.7l.4.4c.1.1.3%200%20.4-.2%200-.3%200-.5-.2-.5-.4%200-.5-.4-.7-.6%200%20.2-.3.3-.2.4v.2l-.5-.1h-.5s-.2.3-.1.4.2.3.4.3h.7l.3-.3zm22.8%2021.1c.2.3.4.4.7.4v.2c.5-.3.5-.3.2-.6v-1c-.7%200-.5.8-.9%201zM12.6%202c-.5.4-.7.8-.4%201.5.8-.3.9-.7.4-1.5zM26%209.2c.1.1.3%200%20.4-.3-.5-.2-.6-1-1.3-1%200%20.7.5%201%20.9%201.3zm21.3%2015%20.6.1.1.4.8.1c.1-.9%200-1-1-.9v-.4l-.2.2-.1-.3c-.5.1-.7.4-.6%201l.4-.2zm5.1%201.1q-.4.7.2%201c.6-.4.6-.6-.2-1zM21%201.8v-.4l-.4-.5h-.4c-.2.1-.3.4-.4.6.4.4.8-.1%201.2.2zM18.1%204c.1-.3-.2-.4-.4-.6q-.6.5-.1%201c.3%200%20.5%200%20.5-.3zm23.2%2015.4s-.2.3-.1.4c0%20.2.2.3.4.3s.3-.2.3-.4V19c-.2.2-.2.5-.6.5zm6.2%202.8c-.4%200-.7%200-.8.2l-.6-.3q.2.4.1.8c.2%200%20.2-.1.3-.2v.1c.6.3.8.2%201-.6zM30.2%202s.2%200%20.3-.2v-.5c-.2-.2-.4-.1-.6%200l-.4.1c-.2.2-.2.4%200%20.6.1.3.4.1.7%200zm1.3%2011-.8.1-.2.4.2.2c.2.1.3%200%20.3-.1%200%200%20.2-.1.2%200%20.4%200%20.2-.3.4-.4v-.1zm1.9-.6c.5%200%20.5-.4.7-.6-.3-.3-.6-.3-.9-.2l.2.8zM22.1%201.7c.3-.2.2-.5.2-.8h-.7c-.1.5.3.6.5.8zM27%207c.2%200%20.4%200%20.6-.2l-.4-.3h-.4s-.1.3%200%20.4l.3.2zm-2.2%204c.2.3.4.5.6.5v.5c.6%200%20.7-.1.6-.4l-.1-.2.4-.6q-.9-.5-1.5.2zm4-3.6c-.2%200-.4%200-.5.2%200%20.2.2.4.4.4l.7-.2-.6-.4zM17%208.3v.2c.1.2.4%200%20.5-.2v-.2c-.1-.2-.4-.1-.6.2zM30.7%2010h.8l-.2-.7-.6.6zm.4%205.5c.2.2.4%200%20.4-.1v-.5l-.4.2.1-.2s-.1-.1-.1%200l-.2.2h.1l.1.4zm-5.3-9.4v.2l.1.1c.3%200%20.5-.2.6-.5-.4-.2-.6%200-.8.2zM24%204c-.1.4.2.5.5.7.1-.5-.1-.6-.4-.8zm11%2017.5q.5%200%20.5-.6a.9.9%200%200%200-.6.6zM23.1%201h.2-.2zm-8.2%203.5c-.3.1-.4.4-.4.7.5-.2.6-.4.4-.7zm8.3-2.2q-.4.2-.3.6l.3-.6zm20.1%2019.5h.5c.1%200%20.2%200%20.3-.2l-.3-.1-.6.3zm5.1%201.2q0%20.4.4.7c0-.3%200-.7-.4-.7zM25%209c-.2-.3-.4-.3-.7%200%20.3.2.5.2.7%200zm15.4%206.3c.3-.5%200-.5-.3-.6l-.2.4.5.2zm-.3-.6zM29.8%208.6q.2%200%20.4-.4l-.5-.4q.2.5%200%20.9zm1.6-7.1zm.1.6-.1-.6-.4.2.5.4zM41.6%2013l.2.7.2-.1c0-.3-.1-.5-.4-.6zM28.9%208.5v.2l.4.1v-.3h-.4zm-5.7.1h.3l.4-.1c-.3-.3-.5-.2-.7.1zm10.6%207.7-.1.2.1.4q.2-.3%200-.6zm7.7%204.3.4.3q0-.4-.4-.3zM33%2017v-.4c-.6%200-.6.4-.9.7l.6.3-.5.7-.3.3c0%20.2%200%20.6.2.7l.8-.1v-.3c.2-.2.3-.4.2-.7-.2-.4-.1-.7-.1-1.1l.3.4c.3-.3%200-.4-.3-.4zM14.7%201h-.1zm27.7%2018.9c.2.2.4.2.6.2-.1-.2-.3-.3-.6-.2zm.6.2zM22.3%204.2v-.3H22v.3h.3zM34.4%2013h.2v-.3h-.3v.3zm23.7.2c-.2%200-.2.2%200%20.4l.2-.3-.2-.1zm.4.8c-.1%200-.3-.1-.5.1h.5zm0%20.1zm.3%2018.9v-4.6l-1%20.2c-.4.5.4%201%200%201.6l-.4-.1-.4.5-.8-.5c-.3.2%200%20.6-.3.8l-.3.2c-.2%200-.3-.2-.5-.4l.4-.2c.2-.1.2-.3%200-.4l-.6-.3h.7c.1-.7.1-.7-.4-.8l-.6-.2.2.2c.3.2.2.4%200%20.6%200%200-.3.1-.4%200a1%201%200%200%200-.9%200h-.1c-.5-.3-.7-.2-.8.3l-.2.2c0%20.5-.4.8-.4%201.4l1%20.1-.2-.4q.5-.3.1-1.1l.6-.1c.3.8.5%201%201.3.7l.8%201%201.5-.4c0%20.4-.2.6-.3%201l.7.4c.5-.1.9-.4%201-1%20.2.2.3.3.2.4a1%201%200%200%200%20.1.9z%22%2F%3E%3Cpath%20d%3D%22m43.2%2021.2.3.2.4-.2c.2%200%20.3%200%20.5-.2l.5.1V21l.1.2%201-.4h.1c.3-.2.6%200%20.9-.2l.6-.2.3-.4-.5-.1v-.2c.2%200%20.4.4.7%200l-.2-.3.3-.3v.3h.7v.6l-.6.3c-.2%200-.4%200-.5.2l-.1-.1c-.1.5-.1.5-.6.9l.6-.1.2-.2v.2l.2-.3h.4v.4c.3-.1.6-.1.8%200H49l.4.4q-.3.8.2%201.2c0%20.2-.2.4-.4.6.5.2.6.1.7-.5.6%200%201-.6%201.7-.5l.2-.2v.4h.1v.7l.6.2v.2c0%20.3.2.5.5.5l.3-.1c.2.5%200%20.8%200%201.1-.2.4-.2.8.2%201H53l-.2.6-.3-.5-.3.5c.6.2%201%20.4%201.3%201l-.3.4c-.4.1-.4%200-.4.6l.6.3.2-.1v-.5h.7c.1-.5.2-1%200-1.3v-.6L55%2028h.4c.8.3%201%20.2%201.5-.4.2-.2.4-.4.4-.6l.1-.3.4-.2.3.1c.2%200%20.5%200%20.6-.4-.2-.1-.2-.4-.4-.6.2%200%20.3-.2.3-.4l.2.1V24l-.1.2v-.4l.1-.1v-2.5c-.5.1-1.1-.2-1.6.2l-.8.6-.1-.4-.4.4h-.1l-.1-.5-.2-.3c.4%200%20.7.2%201%20.4v-.5l.5-.2c0%20.1.1.2.3.2%200-.2-.2-.2-.3-.3l-.5-.4-.2.2.1-.5.7.5c-.1-.3.2-.4.3-.6.3%201%20.4%201%201%20.7l-.1-.5.2.3c.3-.5%200-.7-.2-1-.3.1-.6%200-1-.1l.1-.3c.2%200%20.3.1.3.2.1.3.5.2.6%200l.5-.2v-6.3.5l-.3.8.2.2v.1c0%20.4-.4.7-.4%201l-.1.1-.1-.1-.1-.1v-.4l.1-.3c-.1-.6-.6-.4-1-.5l.4-.6.2-.3-.4-.5h.8l.4-.3-.8-.2-.1-.7-.4.2-.2-.7v-.1c.3.1.5%200%20.6-.2h.2l.5.7a33.4%2033.4%200%200%201%20.3-1l.2-.2v.5h.1V8.2l-.1.2-.2-.4.3-.3V2.8c-.3-.3-.3-.6-.3-1%200%20.2.2.3.3.4V1h-5.4c-.2.2-.3.6-.7.5l-.8-.4h-6.3.2H42v.2h-.2l-.2-.3H39l.2.5-.1.1-.2-.1-.4-.5h-.3v1l.3.5-.3.3.7.4h.1v.1h.5l.3-.3.2-.1c.4-.2.7-.5.7-1%20.5%200%20.4.4.5.7-.2%200-.6%200-.6.4l-.2.2c0%20.3.2.4.6.3l.3.2-.2.4-.7-.2-.2-.4-.8.8-.3.1c0%20.5%200%20.7.5.8.1.2.2.2.4%200l.4.2-.2.4.4-.2.2.4h.3l.2.6v.3l-.5.2-.3.4-1%20.7-.3-.9c0-.2-.1-.4-.4-.5-.2%200-.3%200-.5.2v-.1c-.2-.2-.4-.2-.5%200-.2.1-.2.3%200%20.5l.5.5.1-.2h.2c.4.2.5.5.7.8l-.4.6v-.7l-.4-.2h-.1v.1l-.9.2v.4l.2.2.8-.3.3.4c-.3.1-.4.3-.6.5v.1l-.1-.1-.2.3-.3.1v-.5H37c0%20.1-.2.3-.1.4l-.3.8c0%20.2%200%20.4.2.5-.1.3-.1.6.3.9l-.6.5-.4-.5-.2.5c.5.2%201%20.4%201.2%201v.3h-.2c-.4.2-.4.2-.4.7l.6.3.2-.1v-.3c.3.2.5.4%201%20.2l-.3-.3c0-.1.2-.3.1-.4V14c0-.4%200-.7-.2-1l.2-.1.5%201s.2-.1.4%200h.4l.4.8.6-.7v.1c-.4.3-.4.3-.2.6l.4-.3.5.8c0%20.3.2.5.3.7v.1l-.4-.1-.3.3h-.2v.2l-.8-.4c-.2.1%200%20.5-.2.7l-.2.1-.2.1-.4-.3.4-.2c.2-.2.2-.3%200-.5h-.3v-.3h.4c.1-.7.1-.7-.5-.8l-.5-.1.2.2c.1.1.1.2%200%20.4h-.3v.2h-.2a1%201%200%200%200-.7-.1l-.4-.2-.2.1c-.3%200-.4.1-.5.5l-.2.1c0%20.5-.4.9-.3%201.4l.5.1v.4h.4l-.3.2.1.5c0%20.2%200%20.4.4.5l.3.3.3.1v-.5a135%20135%200%200%201%201.2-1.4c0-.3-.3-.4-.7-.4l-.3.4-.2-.2h-.1l.1-.3h-.7c.3-.2.2-.4%200-1h.6c.2.7.4.7%201.2.6l.8%201%201.5-.4-.3%201%20.7.4c.4-.1.7-.3.8-.6l.4.4c0%20.4.3.7.8%201%20.3-.2.8-.3.7-.9%200-.2-.4-.2-.5-.4l.2-.2h.3c.2%200%20.3-.2.5-.3l.5.3c.3.1.5%200%20.8-.2l.3.5h.4l.3.3c-.1.5-.5.4-.8.5l-.6-.6-.8%201a1%201%200%200%200-.6%200l-.5.8.7.7v.2l-.4-.2-.2-.1h.2c-.1-.3-.4-.4-.6-.6l-.1.3v-.2c-.3-.2-.5%200-.7.2v.5l.5-.3.1-.2v.1c.1.3.2.3.4.3v.4Zm14.6%201.7.3-.1.6-.1h.1c0%20.3%200%20.4-.2.5H58V23h-.3v-.1Zm-.4%201%20.6-.3.1.1.3.3c-.3-.2-.8.5-1.1-.1h.1Zm.4-4h-.3v-.2l.3.1Zm-19.3-8c0-.2-.3-.4-.6-.5l.1-.8c.2.1.2.4.6.4l.3.1h-.1l.5.5c-.3%200-.5%200-.8.3Zm1.4%200-.7-.3.5-.2-.5-.4c.1-.1.2-.3.5-.2l.5.5-.3.6Zm.3-2.3.1-.2.1.3h-.2Zm8.3%202.8c-.4-.2-.8%200-1-.5l.3-.5c.1.4.3.6.8.6l.2.3v.5c-.4%200-.3-.2-.3-.4Zm-1.3%201.3c.2-.1.4-.1.4%200l-.2.2.3.4v.5H47v-1.1ZM47%2010l.5-.4v.6h-.3l-.2-.3Zm1.1-3.8.7.3h-.9l.2-.3Zm-.2-2V4l.2.4H48v-.2Zm.9%208.9Zm.5%201.5v-.2h.1v.2H49l.2-.1Zm-.2-1.3.2.2v.2l-.2-.4Zm.1%202.9.1-.3.2.3h-.3Zm2.2%205.2-.6-.3-.1.1H50l-.1-.5c.5%200%20.6%200%20.6-.4h.4c.1.3.3.6.6.7v.4Zm.4-.8h.3-.3Zm.6-1.2v.3l-.4-.2-.3-.1v-.1c.1%200%20.3%200%20.3-.3-.3-.3-.4-.4-.4-.6%200%20.2.3.4.5.6.3.1.4.3.3.5Zm-.7-3%20.1.1Zm.3%201.4Zm.6-1.5.2.4-.2-.4Zm0-1.5-.3-.4h-.8l.3-.4c.2-.1.2-.3.2-.4l.7.2v-.1h.5c.3%200%20.4-.2.3-.5l-.4-.2.2-.5h.3c0%20.3%200%20.5.3.7V13l.2.5c-.3.3-.4.5-.3.7l-.4.1-.1-.5-.5.7-.3.3Zm-.6-1.6V13v.3l.1.2v-.1Zm.8-3.3a5%205%200%200%201-.3-.5h.2l.2.4v.1Zm2.2%206.8-1.2-.3-.4.3v-.5c.5-.1.5-.2.8-.6.2.2.5.3.7%200l.2-.5h.2v.1l.1.6-.3.6-.1.3Zm.1.6-.1.2h-.3v-.4l.4.2ZM53.2%2015c.2%200%20.2-.1.4-.4v.4l.3.4c-.1%200-.3%200-.4-.2l-.3-.2Zm1.3-.7v.3H54v-.2h.4Zm-.3%200%20.3-.5.2.1c-.3%200-.4.3-.5.5Zm.1-2.3.1.3a4%204%200%200%201-.8-.1c.2-.3%200-.5%200-.7.2%200%20.4-.2.7%200h.1l.3.3.2.2h-.6Zm-.5.6v-.1ZM53%2017v-.2l.1.3-.1-.1Zm.2%201.4-.1-.4c.2-.2.5-.2.4-.5h.2c.6.1.6.1.5.7v.4l.7.8v.3h.1v.4c-.2-.1-.4-.2-.5.1v.7c-.4-.5-1-.8-.9-1.4l.3-.2v.5c.5-.7.5-.8%200-1.2h-.3c-.2.1-.4%200-.4-.2Zm0%204.1c.1-.3%200-.6.3-.9q.2.7-.3%201Zm.4%201.4v-1h.3v.3l.2.2q.7-.2%201.2-.7a1%201%200%200%200-.8%200V22c0-.3-.3-.6-.2-1h.4l-.1.3c-.1.3%200%20.5.4.6.2%200%20.3.2.5.4v.7l-.4.3a1%201%200%200%200-.5.6c-.1.2-.4.3-.7.3v-.5h-.3Zm.5%201.5-.2-.2v-.5c.1.2.3.2.5.3l-.3.4Zm2.7-1.3q-.4-.1-.4-.5.3%200%20.4.5Zm-.8%201h.1l.5.6-.3.5h-.1c-.5-.3-1-.3-1.3.1l-.1.1-.2-.2-.3.2V26h.7c.2-.3%200-.5-.2-.7h.1l.5.2c.2-.1.3-.5.6-.4Zm-.6-10.9h-.3c0-.4.2-.6.5-.7l.3.1-.4.6Zm.3%204.3V18h.2l.1.4h-.3Zm.2-11v-.3l.4-.3.1.3-.1.2-.4.2Zm.3%2010.9.5-.3-.5.3Zm1.2-.4v-.2l.3.2-.2.4-.8-.3h.7Zm-.6-7-.3-.1-.2-.3.4-.4-.1.2.4.2c-.1%200-.2.1-.2.4ZM58%205q-.3-.2%200-.6V5Zm-.8-2.7.1-.1V2c.2-.1.4-.3.5-.6v-.1.1l.1.4v.5c-.3%200-.5%200-.6.2l-.2-.2.1-.1Zm.4%206%20.2.1v.2H57c-.2%200-.4-.2-.6-.4l.2-.3c.3.2.6.4%201%20.4Zm-1-2.8v.8h-.3c-.2-.3.1-.5.3-.8Zm-.9-2%20.4.6q-.4-.3-.4-.5Zm.2%204.6.2.4-.5-.2.3-.2Zm-.3%203.5.2.2.1.3-.6.1-.2-.3c.2.1.3%200%20.5-.3ZM54%205.3h.1c.6%200%20.9-.5.6-1l.5-.1c0%20.6-.2%201-.6%201.2-.2.2-.4%200-.7%200v-.1ZM53.4%201l.4.1-.4.2V1ZM53%206.6l.3.1.5.3v.3l-.3.6.9.6V9h-.6c-.3-.2-.4-.6-.8-.7l.1-.9s0-.2-.2-.3l-.6.3c0-.6.5-.5.7-.8Zm-.5-3.1Zm-.6-.9.8.3h.2l-.5.4c-.2%200-.3-.2-.4-.3l-.2-.2.1-.2Zm.3%205.1.1.5L52%208a3.3%203.3%200%200%201%200-.3Zm-.6%204.5c.2-.3.6-.4%201-.3-.6-.4-.6-.6-.2-1l-.2-.2.3-.3v.1l-.1.3c.1.3.4.4.5.6-.3.4-.3.7%200%201-.1%200-.2%200-.3.2l-.2-.4h-.6v.1a5%205%200%200%200-.3.2v-.3Zm-.4%206c.3%200%20.5.2.4.4H51c-.1.1-.3.2-.4%200l.3-.3h.2ZM51%208.1l-.1.1-.1.2c-.4%200-.6.4-1%20.7l.3-1c.2.2.6-.1%201%200Zm-1.1-5.3c0-.3.4-.4.6-.5l.1-.1h.1l-.2.6-.1-.1-.2.1h.1l-.5.3v-.3Zm-.3%202%20.1-.1.2.2-.3.5-.1-.2.2-.2-.1-.3Zm0%201.6c.5.5.4%201-.1%201.3-.3-.3-.3-.6-.4-1h.3c0-.2.2-.2.3-.3Zm-1.1-5c.2%200%20.4-.1.5-.4.2%200%20.3.2.3.5-.2%200-.4%200-.6.3l-.3.2-.2.2v-.6H48l.5-.1ZM48%202.8v1.1c-.5-.3-.5-.5%200-1.1Zm-1.2%204.7.7.1.2-.6.4.1-.4%201.8-.1.1a3%203%200%200%200-.4-1.2l-.1.4.1.4v.3l-.3-.2.2.5-.4.1.1-1.8Zm0%208.7c0-.1.1-.2%200-.4h.4v.5h-.5Zm-1.5-2.5-.1-.2-.1-.3c.2-.1.3-.4.3-.6.2%200%20.3%200%20.5-.2l.5.5c-.3.2-.5.5-.8.6l-.3.2Zm0%20.8h-.2l.1-.2.1.2Zm0-4.4c0-.2%200-.3.2-.4v.4h-.2Zm.3-7.8c.2.2.2.3%200%20.5v-.5ZM45%203.6l-.2.1v-.4l.2.3Zm-.2.3.5.5.7-.2.3.3-.3.3h-.8l.1.2-.1.2h-.1v-.4l.2-.4-.5-.2v-.3ZM45%206v-.2l.2-.3.2.2c-.2.4%200%20.6.4.9l.6.2-.3.7-.3-.1-.4-.1h-.3l-.2-.2h-.2c.4-.2.6-.6.4-1Zm-1-3.9V3v-.1l-.2-.7h.2Zm0%207.9.6.2h.4v.2c-.2.1-.4.2-.7.1l-.1-.3-.4.3-.3.2-.1.5-.4-.4v-.5c.5.2.7-.2%201-.3Zm.2%205.2v-.6c.4.2.2.4%200%20.6Zm-.9-6.4h.4V9l-.4.3v-.5ZM41.8%205c.2-.3.5-.2.8-.4l-.1.3.2.2-.4.2c-.3%200-.5%200-.7-.2h.2Zm.4%201.9h-.4l.1-.6.5.1v.2h-.2V7Zm-.8%201.7.2-.1c.4%200%20.8%200%201-.6%200-.1.2-.3.4%200v.5c-.2%200-.4%200-.6.2a1%201%200%200%201-.5.2h-.2l-.2.1c0%20.5%200%20.7-.2.9-.1%200-.3%200-.5-.2.7-.1.4-.7.6-1Zm.6%209v-.1h.1Zm1.7-3.7-.9.2-.4-.8-.5.4h-1l-.4-1%20.7-.5.5.1c.5-.2.3-1.2%201.2-1v.6l.1.1v.3c0%20.2%200%20.5-.2.8.4%200%20.7-.1%201%20.2h.4v.8l-.2.2-.3-.3Zm2.5%202.6-.4-.4-.2.5-.2.2-.4-.3h-1l-.2-.3.2-.4h-.2l.9-.4-.2.4c-.1.1-.3.1-.4.4l.2.2.5-.1.3.2c.3-.2.5-.3.5-.5l.5-.5v-.3h.1l.4.2c-.1%200-.3.1-.3.3-.2.1-.2.3%200%20.5h.1l-.2.3Zm.2%201%20.3-.8c0%20.3%200%20.5.2.8l.5-.3.2-.4a7.8%207.8%200%200%201%20.4.6v.1c-.3.3-.2.8-.6%201v-.3c0-.4-.2-.6-.5-.7h-.5ZM29.2%201h.5-.5Z%22%2F%3E%3Cpath%20d%3D%22M34.7%201.4V.9h-4.1l.2.4.3-.3c-.1.2%200%20.4.3.5v-.2l.5.3-.2.8c0%20.5-.2%201%20.1%201.4v1.4l.6-.1c-.2.2-.1.5%200%201v.3s-.2.1-.2%200h-.3l.2-.3c-.3%200-.6-.1-.8.2-.1.1%200%20.3%200%20.4l-.1.4c-.1.2-.4.3-.6.4l-.5.3c.4.2.7.4%201%20.1h.4c.1.6.3.7%201%20.8V8h.3c0%20.3%200%20.4.4.7l-.4.6c.5.1.5.1.7-.5.3%200%20.5-.2.8-.3l.1.5.6-.8h.2l.2-.2.2.1.2-.5.2-.2h.6c0-.6.7-1%20.6-1.7%200-.2-.2-.4-.4-.4H36l-.3.4v-.2c-.3%200-.2.2-.2.3-.3-.1-.6-.2-1%200l.2-.2c.4%200%20.6-.3.7-.7%200%200%20.2-.1.2-.3v-.2q-.4-.4-.1-1c.2%200%20.4%200%20.4.4%200%20.3.2.5.5.6.2-.2.2-.4%200-.6.1-.4.7-.3.6-.7l-.5-.5c0-.3%200-.5.4-.7.5-.1.5-.2.9-.8-.3%200-.5%200-.7-.2H35c0%20.2%200%20.3-.2.5Zm1%204.4h.1Zm0%200h.1v.3-.2Zm0%20.2c0%20.2-.1.3-.2.3%200%200%200-.2.2-.3Zm-.7.7h.3c.2%200%20.3.2.2.3l-.3.2H35v-.5Zm-.9-1.2.4.2-.4.2v-.4ZM33%207v-.3l.1.2-.1.1Zm-.3-4.7.4-.9q.5.3.7%201.1l-.7.2-.4-.4Zm.5%201.9.3-.3c.3%200%20.4.2.5.5-.4%200-.6%200-.8-.2Zm1.5%202.7h-.2c-.2%200-.2.7-.7.3l-.2-.7c.4%200%20.8%200%201.1.4Zm.7-4.7.8.2.1-.3c.3.3.2.4-.3.8l-.6-.3v-.4Zm-.2%202a.7.7%200%200%200-.6-.1l.3-.3.3.3Zm23.6%208.1v-1%20.2c-.3.4-.3.6%200%20.8ZM52.8%201h-.2l.1.1.1-.2Zm6%2019.5v-1%201Zm-9.4-5.9Zm-4%2012.2V28c.8%200%201-.2.8-1v-.6l.3.1c.3-.3.4-.5.2-.7l.5-.3q-.5-.4-1-.1c0-.1%200-.2-.2-.3l-.4.5-1.3-.6v.4c-.2.4-.5.8-.5%201.1%200%20.3.4.6.6%201%20.4%200%20.7-.1%201-.6ZM34.4%209Z%22%2F%3E%3Cpath%20d%3D%22M34.2%209.8c0%20.2%200%20.5-.2.7v.2h-.1l-.1.6c.4%200%20.5-.3.7-.5l.4.2h.1c.3.2.4.4.5.7l.3.3c.2-.4%200-.8%200-1.2h.2l-.1-.3v-.2l.6-.2v-.3l.3-.4c0-.5%200-1-.3-1.4h-.2v-.5c-.2.2-.3.3-.1.5-.7%200-.8.3-.7%201.1l.8.3v.3h-.5c-.1-.2-.3-.4-.5-.2l-.3.1c-.1-.3-.1-.6-.6-.6-.3.2%200%20.5-.2.8Zm15.9%2018.4c.5.2.6-.2%201-.4-.3-.3-.5-.6-.8-.7a1%201%200%200%200-.3-.1l.4-.2v-.3h-.2l.3-.4c-.2-.3-.5-.3-.9-.3l.2.8h.1v.4h-.6c-.5-1-.4-1-1.6-.5.2.5.4%201%201.1.9.2.3.1.7.5.8.3%200%20.5.1.8%200ZM40.4%2019l-.5-.1c.2-.3.4-.7%200-1.1L39%2019h.4l-.6%201-.3.1-.3.4c0%20.1.2.3.4.3.2.1.4%200%20.4-.2l.2-.2h1.4l-.1-1.4Zm3.6%204v-.2c0%20.2.1.3.4.4l-.1.6.4.1-.1.8c.7.3.7.3%201.3-.5l-.2-.1-.3-.2.6-.4-.5-.1c-.5%200-.8-.2-1-.8h.6l.3.5h.3v-.3h-.3c0-.2%200-.3-.2-.4a.7.7%200%200%200-.7%200c-.1-.2-.3-.3-.6-.3v.3c-.5-.1-.5.4-.7.5q.3.2.7.2Zm9.7%208.4-1.1.8.1.4c.1.3%200%20.5.4.6l.3.3.3.1v-.5c.4-.1.7-.2.7-.6l-.7-1ZM37.9%204.7c0-.2-.1-.3-.4-.5v1.2l.2-.3.3.3s.6.5.8.5c.5.1.6.5.7%201l.2-.3.2.2.7-.2-.6-.5c.1-.2%200-.3-.4-.7l-.6.3-.1-.4h.1V5l-.2-.1c-.1-.3-.3-.5-.8-.5l-.1.3Z%22%2F%3E%3Cpath%20d%3D%22M35.8%2013.6c.2.2.3.5.2.7l-.3%201h.4l.3-.6-.1-1v-.3l-.6-.5c0-.2%200-.5-.2-.6l-.2-.1-1%201-.4-.4-1-.1c-.5-1-.4-1-1.6-.5l-.1-.2.5-1%201.2%201.3.4-.3-.4-.4.2-.4-.7-.4v-.3l-.1.2c-.4%200-.4-.3-.5-.6l-.3.3-.4-.4v.5a1%201%200%200%200-.4.5c-.4-.3-.4-.3-.8%200l-.3-.3-.4.5-1.3-.6v.4l-.5.9c0-.3-.1-.5-.4-.7-.2-.1-.5%200-.8.2l.4.7h.8c0%20.3.4.6.6%201%20.3%200%20.7-.1%201-.6v1.1c.8%200%201-.2.8-1%200-.8.2-1.2.9-1.5v1c0%20.3.3.6.8.7v-.2c.2.3.4.5%201%20.4%200%20.3%200%20.6.2.8h-.2c0%20.6%200%20.6-.5.7%200%20.3.1.5.5.5.3%200%20.2-.3.3-.5l.6.6c.4-.2.5-.5.4-1V14c.3.1.4%200%20.6-.3.3.1.6.1.8.3l.5-.4h.2zm-2.6.4zm21.2%2021c0-.1-.1-.2-.3-.2s-.4%200-.4.2l-.1%201.3H53c0%20.5.3.8.8%201%20.4-.3%200-.6%200-.9.6-.3.5-.8.6-1.3zM19.6%201h.2-.8.6zm32.6%2023c0-.2-.3-.4-.5-.2s-.3.1-.6%200c0%20.5-.2%201%20.3%201.5l1-.2-.2-1.1zm-5.7%206v-.9l-.4.1c0-.2-.1-.4-.5-.7-.2.3-.2.6%200%20.9-.3.1-.3.4-.1%201%20.4.2.7%200%201-.3zm-.1%203.5c.3.2.6%200%20.8-.1.5-.3.1-.8.3-1.2-1.3.2-1.4.4-1%201.3zM31.5%2021.6c.8-.5.8-1%200-1.4-.6.8-.6%201%200%201.4zm17.2.1-.8.2c.1.9.2%201%201%201%20.3-.4-.2-.8-.2-1.2zm-20.1-3.9c.8-.3%201-.7.5-1.5-.6.4-.7.8-.5%201.5zm19.8%2015.1c-.1.2%200%20.6.2.6h.7v-1c-.4.1-.8%200-1%20.4zm-5.5-9.8c-.3%200-.4-.2-.5-.4l.1-.3-.3.2a1%201%200%200%200-.5-.4c0-.5%200-.6-.6-.8%200%20.6%200%20.7.4.9%200%20.5.6.8%201%201.1%200%20.2.2%200%20.4-.3zM56.4%2032l-1.1%201.3h1c.2-.4.4-.7%200-1.2zM33.3%2017.5l.2.3h.4c-.3.4-.3.5.1%201%20.3%200%20.5-.2.6-.5%200-.2%200-.3-.2-.5.1%200%20.3%200%20.4-.2-.5-.4-1-.3-1.5%200zM58%2034.4c.2%200%20.3-.2.3-.4v-.8c-.1.1-.2.4-.6.5%200%200-.1.3%200%20.4l.3.3zm-8.3-2.6.2.3h.8l.5-.2c-.5-.4-1-.3-1.5-.1zM48%2027.4h-.8l-.2.4.1.2c.2%200%20.3%200%20.4-.2h.2c.3%200%20.2-.2.3-.3v-.1zm10.2%209.2c0-.7%200-.8-.7-.9%200%20.6%200%20.6.7%201zM24%207c-.2-.2-.4-.1-.6%200v.6c.3.1.4.2.6%200s.2-.4%200-.6zm18%2018.6c-.2%200-.2.1-.1.6.5%200%20.6%200%20.6-.3%200-.2-.2-.3-.5-.3zM24.4%201.2l.1-.3H24c0%20.1%200%20.2.2.3h.3z%22%2F%3E%3Cpath%20d%3D%22M30.2%2010.8c.2-.2.2-.5%200-.6h-.3c-.2.1-.2.5%200%20.7l.3-.1Zm14.6%2011.1c0%20.2.1.4.3.4l.7-.3-.6-.3c-.2%200-.3%200-.4.2Zm-11.5.6.1.3c.2.1.5%200%20.6-.2v-.3c-.2-.1-.5%200-.7.2ZM48%2029.7v-.5c-.3%200-.4.1-.5.2v.4c.2.1.4%200%20.5-.1Zm7.9%207.1c-.2%200-.2.4%200%20.6h.3c.2-.2.1-.4%200-.6h-.4ZM37.5%202.2c-.3.3-.3.6-.2.8.5-.2.5-.3.2-.8ZM41%2019c0-.5-.2-.7-.5-.8-.2.4.1.6.4.8Zm10.3%2016.8q.7-.1.6-.6c-.3.1-.5.3-.6.6ZM39.7%2014.7Zm-.1.6c.4-.3.4-.3.1-.6-.3%200-.4.3-.1.6Zm17%2013.7Zm.4-.7c-.6.3-.6.3-.4.6l.4-.4v-.2Zm-8.1-3.5c0%20.3-.7.3-.4.8.4-.2.3-.5.4-.8Zm-17.6-6c-.3%200-.3.3-.4.6.5-.2.6-.3.4-.6ZM30.1%208.4l.2.7.3-.5s-.2-.2-.5-.2Zm11.4%2014.8c-.2-.2-.5-.2-.8%200%20.3.3.5.3.8%200Z%22%2F%3E%3Cpath%20d%3D%22M56.8%2029.5c.4-.4%200-.4-.2-.6l-.2.5.4.1Zm-.2-.5Zm1.4-1.7.3.6h.1c0-.3%200-.5-.4-.6Zm-18.3-4.8h-.3v.6h.4v-.2h.1l.4-.2h-.5v-.2Zm-6.4-12.3.5-.5c-.6%200-.6.2-.5.5ZM38.5%203h-.3v.3h.3V3Zm11.6%2027.7.2.4q.2-.3-.1-.5l-.1.1Zm7.8%204.1.5.4q0-.4-.5-.4ZM37.1%204.1l.3-.1v-.2h-.3v.3Zm-4.5%206.2v.3h.3l-.1-.4h-.2Zm26.2%2026.5-.4.2h.4v-.2Zm-9.4-5.5.3.5c.3-.3%200-.4-.3-.5Zm9.3%203.3v.6l.1-.1v-.4h-.1Zm-20-16.4h-.2v.3h.3l-.1-.3ZM51%2027.3V27h-.2v.3h.2Zm-7.5-13.5v.1h.2v-.3l-.2.2Z%22%2F%3E%3C%2Fg%3E%3Cpath%20fill%3D%22%234db6ac%22%20d%3D%22M59%2021a3%203%200%200%200-.5-.4%204.4%204.4%200%200%200-3.8.1%206.5%206.5%200%200%200-3.2%203.3c-.3.8-1%204.6-.4%205.2-3.1-3.7-8.9%200-6.6%204.6-2.6%200-6.2%201.9-4.4%205.1-3.5-1.6-6.6.4-6.6%204-3.4-1.7-5.7%203.4-5.2%206.1%201-.4%202.7%200%203.7%200h11.8c4.3.1%208.9.6%2013.1.2.7%200%201.5%200%202.2-.2V21Z%22%2F%3E%3Cg%20fill%3D%22%2326998b%22%3E%3Cpath%20d%3D%22M51.1%2042.5zM49.3%2049v-.2l.2-.1v-.3c-.1-.2-.3-.2-.5%200l-.4.2h-.3l-.2-.2c-.2%200-.2.2-.2.3l.1.4v.1h1.4v-.1h-.1zm-12-2c-.2.2-.3.4-.2.7l-.4.2v.2c-.2.2%200%20.4%200%20.6l.2.1h.6c.2%200%20.2-.1.2-.2v-.7c.2-.2.2-.4.2-.7-.3.1-.4-.1-.6-.2zm6.9-4.6.2.2.2.3-.4.1c0%20.4%200%20.4.3.5l.1-.1.3.2.1-.2v-.5l.4-.5h-.3V42c-.2%200-.2-.1-.3-.2h-.5l-.1.2-.1.2.1.2zm-1.8%204v.3l.4-.1v.3c.2%200%20.3-.1.3-.3v-.3c.1-.1%200-.3.2-.4%200-.2-.2-.3-.4-.4h-.4l-.1.1-.1.1a.42.42%200%200%200%200%20.7zm4.1-1.5h.4l.1.3-.1.1v.2c.2%200%20.3%200%20.4-.2V45s.2%200%20.2-.2q.2-.2%200-.3h-.1s0-.3-.2-.3l-.3-.2-.2.1-.2.3h-.1l-.2.2.2.2v.2zm-6.9.2c0-.2.2%200%20.2-.2l.3-.3-.3-.2-.3-.1h-.6l-.1.2v.2c0%20.2%200%20.3.2.4l-.2.2.1.2c0-.2.2-.2.2-.3h.5zM51.4%2047c.1%200%20.2%200%20.2-.2v-.3c.3%200%20.3-.2.2-.3l.2-.2c0-.2%200-.3-.2-.3l-.1.2c-.3%200-.4.3-.7.3v.9h.4zm-1.6-7.6h.2v.6l.4-.2-.1-.3h.2l.2-.3h.7v-1H51c-.2%200-.3%200-.4-.3l-.3.2v.5h.1v.3l-.2-.1c-.1%200-.3%200-.3.2v.2h-.4c0%20.2%200%20.2.2.3zm-8.3%206.2.4-.2c.2%200%20.3-.1.3-.3l-.5-.1.2-.3c-.2%200-.4-.2-.5%200-.2%200-.2.2-.3.4h.5v.5zm7-7%20.2.3v.1l.3-.3c.3-.1.3-.4%200-.6-.2-.1-.3-.1-.4%200l-.2.4zm.5%201.2v-.2h-.2c0-.4-.2-.5-.5-.6-.2.3-.1.6%200%20.7.2.1.4.2.4.4%200%20.1.1%200%20.2%200q-.2-.2-.1-.3s0%20.1.2%200z%22%2F%3E%3Cpath%20d%3D%22M52.4%2047.2c.1-.2%200-.4-.2-.5H52l-.1.2-.2-.2s0%20.2-.2.3l.1.1v.4l.1.2h.2l-.3.1.2.3v.2l.5-.1v-.5l-.2-.2-.2.1.1-.2.4-.2Zm-3.2-4.6c0%20.1%200%20.2.2.2l.4-.1v-.5a.6.6%200%200%200-.4-.1l-.2.1v.4Zm-3.7-3.8.4.2v-.3c.1-.1%200-.3%200-.4h-.4v.5Zm3-1.6v-.5c-.4%200-.5%200-.6.2l.2.3q.2.1.4%200Zm-.3%204.1h-.3v.2s0%20.2.2.3h.2c.2%200%20.2-.2.2-.3%200-.2-.2-.2-.3-.2Zm.8%206.3c0%20.1%200%20.3.4.4v-.2c.1-.2.1-.2%200-.4l-.4.2Zm4.8.7h-.5l.1.3h.2l.1.1c.2-.1%200-.3%200-.4Zm0%20.4zm-16.2-5.4c-.2-.1-.3%200-.5.1l.2.3c.3%200%20.3-.2.3-.4Zm2%20.1.1.2c0-.3-.1-.4-.2-.5h-.3c0%20.3%200%20.3.4.3Zm13.2-.9c.2-.2.2-.2%200-.4l-.1-.1c-.3.2-.2.3%200%20.5Zm4.6%206.6h-.2v.1h.7c-.2-.2-.3-.2-.5%200Zm-11-.2-.3-.1H46c-.2.1-.2.2-.2.3h1l-.2-.2h-.1Z%22%2F%3E%3Cpath%20d%3D%22M58.8%2037.6v-.1c-.1-.1-.3%200-.4%200%200-.3.2-.1.3-.2V37c-.1-.3-.2-.3-.5-.3-.1%200-.3%200-.4.2-.2.2-.2.3-.1.5h-.2l-.4-.4v-.7c-.2-.2-.4-.2-.5-.2h-.4c-.2-.1-.2-.1-.4%200V36h-.3l-.3-.3c.2%200%20.4-.1.5-.3h.1c.2%200%20.3-.1.3-.3V35l-.3-.1a2%202%200%200%200-.5.1l-.2.3-.1.4-.2.1v.7l.4-.2c0%20.2%200%20.4.2.5l.2-.3.2-.3c0%20.1%200%20.2.2.3h.1l.1.6-.2.1v.2l-.1.1h-.2l-.4.2.2.1c0%20.1-.2.2%200%20.3l.3.3h.2s.1%200%200%20.2c-.1%200-.1.2%200%20.2v.7h.1v.1l.2.2h-.6v.2c0%20.2-.1.2-.3.2%200-.3-.1-.5-.4-.6%200-.2%200-.3-.2-.4l-.1-.1c0-.1%200-.2-.2-.3h.1l.4.2s0-.2.2-.2c.2-.2.3-.3.2-.5l-.2.1-.3-.2-.2.1v.1c0-.1%200-.4-.2-.6%200-.2.2-.1.3-.2v-.3c.1%200%20.3%200%20.4-.2h-.3l-.3-.2h-.2c-.2-.1-.3%200-.4.2v.3l.2.3-.3.1h-.1v-.2l.2-.2h-.3l-.3.1v.5h.1v.3H53c-.2%200-.2.2-.2.4h-.1c-.2.1-.2.2-.2.4h.3l.1-.2H54l.1.4v.3l.1.3h-.3l-.1-.4.1-.2-.3-.2-.4.2v.2l.5.4-.3.3v.4l-.2.2v.1l-.2-.3v-.1c.1-.3%200-.5-.1-.7-.1.1-.3.1-.4%200h-.2v.3c-.1%200-.1.1%200%20.2v.6H52v.2c0%20.2%200%20.4.2.5v.2l.2-.1h.3l.4.5-.1.1c0%20.2-.1.2-.2.3v.1l-.1.5-.4.2a1%201%200%200%201-.1%200v-.5l-.1-.2v-.1c0-.1-.1-.1-.2%200h-.2c-.2%200-.3%200-.4-.2-.1-.2-.2%200-.3%200%200-.2%200-.4-.3-.5l.2-.2h.3c.1-.2.1-.2%200-.4l-.4.1v-.3c-.4%200-.6%200-.6.4.2%200%20.2.3.4.4l-.2.2v.4l.1.1v.2l-.2.1h-.5v-.1h-.2c0%20.2%200%20.2-.2.3v.1c0-.2%200-.3-.2-.3l.1-.2h-.1l-.3-.2-.2-.2c-.2-.1-.3-.3-.6-.2l-.3-.2-.4.1c-.1-.2-.3-.2-.4-.2l-.2-.1h-.3c-.3%200-.3.4-.2.6v.3c-.3.1-.3.3-.4.5l.2.2v.2l.3-.1.1-.2.3-.2h.1v-.6h.4V42c.2.1.3.3.3.6-.1.2%200%20.3%200%20.4h.1l.1.2c.2-.1.2-.2%200-.2l.1-.2-.1-.5h.2v.2l.1.3.2.2c0%20.2.2.3.3.4h.2v.4c0-.4-.1-.4-.4-.3l.1.8-.2.3v.1h.2c.2.2.3.2.4%200v-.1l.1-.2.3.1.2.1v.1l.1.1.2.2h-.2l.2.8-.3.1v-.2c-.2-.2-.5%200-.6-.3-.2%200-.3.2-.3.3%200-.2%200-.4-.4-.5q.2%200%20.2-.3H48l-.1.3h-.2l-.2.1s0%20.2-.2.3l-.1.2c0%20.2%200%20.3.2.4l.3-.1c.2%200%20.2-.2.2-.4v-.4h.2l-.1.2c0%20.2%200%20.3.2.3h.3l-.3.2h-.1c-.2%200-.3.1-.3.3v.3h-.2l-.4.1v-.2l-.1-.3h-.4v.5l.2.2h.2c0%20.2.1.3.3.3v.6c.1%200%20.1.1%200%20.2v-.2l-.2-.2c.1-.1.1-.3%200-.4h-.3v.6l-.2.6.2.2.2.1.2.1c0%20.1%200%20.1.1%200l.1.2h.2c.2-.3.2-.4%200-.6V48c.2.1.3.2.5%200v-.2c.2%200%20.2-.2.2-.3v-.1c.2-.2%200-.4.1-.6l.2.1c.1.2.2.2.4.1h.1l.2.2c.2.1.3.2.5%200h.3l-.1-.7h.1c.2%200%20.3-.1.3-.2V46h-.1c0-.2.1-.2.2-.3h.2l-.1.3h.4l.3-.3-.4-.2-.3-.5q0-.4-.3-.5v-.2l-.1-.7c.2.1.4%200%20.6.2h.1l.1.1c0%20.2.2.2.3.2v.2h-.2l.2.1.1.3h.2v.7h-.2V45h-.7c.2.3.2.3.5.3v.3h.3l.3-.1.3-.1v.2c-.3.2-.3.3%200%20.5v.2h.2l.3.2.1.2.3.2h.1v.5s-.2-.2-.4%200l-.2.2c-.2.1-.2.2%200%20.4h.2l.3.3c.2%200%20.3-.3.5-.2V48h.1v.1q0%20.2.2.2v-.2h.1l.2-.1c-.1.2-.1.3%200%20.4l.3-.2c.2.2.2.3.3.2h.3l-.3.2-.2.2v-.4H54l-.2.3c-.3%200-.4.2-.5.4h-.1v.2h.5l.1-.1.1.1h.5V49l.2-.1-.1.4%202.4-.1.2-.2h.1l.2-.1.1-.3c0-.2.2-.3.3-.3l.4.2v.1c-.1%200-.3%200-.2.1l.1.2.2-.1h.1v.2h-.1.7v-.8l-.2-.2h-.2.5v-2.2H59v-.1h.2v-2.2H59v-1c0-.2%200-.2-.2-.3v.1h-.2v-.2h.5l.1.2v-1.8H59l.1-.2v-2%20.1-.6c-.1%200-.2%200-.2-.2ZM49.4%2044h-.2l.2-.2v.2Zm-1.5%203v-.1Zm1.4-.5Zm.2%200v-.3l.2.2h-.2Zm.3-1.4V45Zm.5%200v.2-.1Zm.2-2-.1-.1h.1v.1Zm.6-.2h.2-.2Zm1.2%202.3Zm.6-.9s0-.2-.2-.2l-.4.1-.2-.2-.4-.1c0-.1%200-.2.2-.2s.2.3.5.3l.1-.3h.2l.1.2h.3c0%20.2.1.3.2.3-.1.1-.2.2-.4.1Zm.3%201.4Zm5.2-6.6.2.1-.4.2.1.2H58v.4h-.2v-.2l-.2-.4v-.2h.1c0%20.2.1.2.2.2%200%200%20.2%200%20.1-.2l.4-.1Zm-.5-1.4h.1s0%20.1%200%200h-.1Zm-.3%201h.1l.1-.2h-.2v-.1h.4v-.1h.1l-.1.4-.2.3v-.4Zm.3%202.5v.2h-.2l-.1-.2h-.1c0-.1.3%200%20.4%200Zm0%20.3v.1h-.4l.2-.2v.1h.2Zm-.8-3.7Zm-.2.3.2-.3v.2c0%20.2%200%20.3.2.4h.1v.3l-.3.1.1-.3H57v-.3h-.1Zm-.3%204.6h.1l.2-.2h.4v.5l-.5.2-.2-.5Zm.2.6h-.1Zm.1-1.3v.2h-.2l.2-.2Zm-.3-4.8Zm-.5%203.6.2.2v-.3c.2-.1.2-.3.1-.4V40c0-.1.1-.1%200-.2v-.2l.1-.2c.2%200%20.3%200%20.3-.2V39h.1v.1q-.3.4-.2.7l-.2.2h.4l-.2.2v.5c0%20.2.2.3.4.4v.1l-.2.2v-.2l-.3-.1c-.2%200-.3-.2-.5-.3Zm-.4%201v.1Zm-1.2-1.2.3.1h.3l.1.1.1.2v.2c-.3%200-.3%200-.3.2.1%200%20.2%200%20.3.2l-.1.2h-.1l-.2-.3V41c0-.2-.2-.3-.4-.2v-.3Zm-.2-.5v.1l-.1-.1Zm-.3%201.4v.2-.2Zm-.5%202v-.1Zm.7%202.8h-.3l.2-.2.4-.2c0-.1%200-.3-.2-.4l.1-.3V45c0-.1%200-.2-.2-.3v-.1l.4.2v.5l.2-.1v.2c.1%200%20.2%200%200%20.2h-.2v.3l.1.2.3-.1v-.1h.2v.3h.1v.2h-.4v-.1c-.1-.1-.2-.2-.4-.1l-.2.2Zm-.3-.9h.1Zm.3-1.8Zm.1%203.2h.1Zm.8%201.4h-.2l-.1-.1-.2-.1-.2-.1v-.7.4h.2c0%20.2.2.2.3.1l.2-.1v.2l.1.5h-.1Zm.6-.6-.4-.2h.2c.2%200%20.3-.1.3-.3h.1l.3.1-.4.4Zm.5-1v.1H56v-.4h.3c-.1%200-.2.2-.1.3ZM56%2046v-.1l.2.1H56Zm.2-.5c-.1%200-.2%200-.2.2h-.1v.1l-.3-.1V45l.3.1h.3v.2Zm-.2%203.7h-.1Zm0-.7v-.2h.3v.1l-.3.1Zm.3-2.4.1-.2h.1v.3l-.2-.2Zm.1-1.3h.3l-.1.1h-.1Zm.6%202.5c-.2.1%200%20.2%200%20.4l-.3.1-.1-.3h.1v-.1h.1l-.1-.3.2-.2c0%20.2.2.2.3.3H57Zm-.3-1.5h.4-.4Zm.5.9H57v-.2h.2l.2.2H57Zm.6-1.3v.2l-.3.3c0-.2-.2-.3-.4-.3V45l-.3-.3v-.2h.5v.1l-.2.2h.2v.4h-.1c0%20.3.1.3.3.2v-.2h.3v.1Zm0-1.1-.2.2v-.1l.2-.1Zm0%20.7-.2.1.2-.1.1-.2.4-.1.1.2H58v.2h-.2Zm.5%203Zm0-.1-.2-.1v-.1l-.1-.2.1-.2V47h.3v.6l-.1.2Zm.7-1.3v.2c-.2%200-.2.1-.2.2l-.4-.1v-.4h.3l.3.1Zm-.4-2.7.1.1v.1l-.2.3h-.1a.4.4%200%200%200-.4-.1v-.4l-.3-.3h-.5l-.1.1-.2.1v.2l.1.3c-.2%200-.3-.2-.4%200h-.2v-.1H56l-.2.1h-.3v.2h-.2v.2h-.1l-.4-.1.2-.2v-.1h.2v.1h.3l-.1-.3H55v-.4l-.4-.4-.1-.2h-.2a8%208%200%200%201-.2-.4c-.3%200-.5%200-.6.2v-.3c0-.2%200-.3-.2-.4v-.1c.2%200%20.3-.1.3-.2v.3h.3l.2.2.3-.1.1-.1h.3c-.2%200-.2.2-.2.4h.2c.1.2.3.1.4%200v-.1l.2-.2h.3V42l.2-.1.1.1-.4.5h.2l-.2.2v.1l-.4-.1-.2.1h-.2c0%20.3%200%20.4.3.5V43l.2.1c0%20.2.2.2.3.2h.2v.5h.1l.2-.2h.2l.1.1.1-.1h.7l.2-.3h.2l.3.3h.4c.1.2.2.2.4.1Zm-2.8-.8Zm2.6-1.2-.1-.1.1.1Zm.3-.6-.2.1c-.1-.3-.4-.3-.6-.3l-.2-.5h.2l.2-.2v.1l.1.3.2.2c.1-.2.1-.3%200-.4h.4c0%20.3-.2.5%200%20.7Zm.2.6v.1Z%22%2F%3E%3Cpath%20d%3D%22M52.8%2049.2h-.2V49h.2c.4-.1.4-.4%200-.6h-.6l-.4-.1h-.3c-.1.3-.1.3-.3.2v-.2c.1%200%20.3-.1.3-.3l-.2-.1v-.2c0-.2-.1-.2-.2-.3H51l-.1-.1v-.2c-.2%200-.2%200-.1.3l-.2.2h-.1v-.1c.2-.2.2-.2.1-.4h-.2l-.1.5-.4-.1-.1.1.4.2c-.2.1-.1.3%200%20.5v.4H50v.2h.1l.2.2v.1h2.5Zm-1.4-.2.2-.1v.2l-.2-.1Zm-11-2v.3c.3%200%20.4-.1.5-.3h-.5Zm2.8-1.4h.1c.2.1.3%200%20.4-.1-.2-.1-.3-.1-.4%200ZM43%2045l-.4-.3h-.2l.5.4.1-.1Zm8.6-3.4zm.1.1h.2s.1%200%200-.2h-.3v.2Zm-15.8%204.8c-.2%200-.2%200%200%20.3l.3-.2c-.2-.2-.2-.2-.3-.1Zm13.8-10.7v-.3c-.1-.2-.2.1-.3%200v.2h.3Zm-2.1%203v-.3h-.3q0%20.3.3.3Zm-9.2%207.3-.2.4.2.1c.2-.1.1-.3%200-.5ZM50%2042c.2%200%20.3%200%20.2-.3H50v.3Zm-5.7%201.9-.1.3h.2c.1-.2%200-.2-.1-.3Zm-4.4%201.7zm-.4%201.4.1.1c.1%200%20.2%200%20.3-.2l.1-.1c.2-.1.3-.4.3-.6V46h.3l.1-.3c.2%200%20.3.1.4%200l-.2-.1-.2-.4-.1-.1a.3.3%200%200%200-.5%200l-.2.3v.4h-.3c-.2-.2-.5%200-.6.2v.5c.1%200%20.2.3.4.3h.1Z%22%2F%3E%3Cpath%20d%3D%22M39.8%2045.4h-.2v.3h.2c0-.2%200-.1.1-.1l-.1-.2zm1%201.1v-.1c0-.1-.1-.2-.3%200l.2.2.1-.1zm-2.4-.7h-.3v.3q.2%200%20.3-.3zm3.4.5c0%20.2%200%20.2.2.3%200-.3%200-.3-.2-.3zm-1.4-1.9-.1.2h.4s-.1-.2-.3-.2zm2.9-.2v-.3l-.2.1v.1h.2zm-4.8-.2q-.3%200-.1.2v-.3zm11-3.5c.1.2.1.2.3%200h-.3zm2.2.5c-.2%200-.2%200%200%20.2V41zm-.4.9s.2.1.2%200v-.1h-.2zm-1.7-2.3h.1v-.2h-.3v.1c0%20.1.1.1.2%200zm-3%206.4v.2c.2%200%20.2%200%20.3-.2h-.3zm1.3-7c-.1-.1-.2-.1-.2%200l.1.1c.1%200%200%200%200-.2zm3.1%208.3c.3.2.3.2.4%200h-.3zm1.9%200v-.2h-.1l-.1.1.1.2zM47%2043.8l.1-.2c-.2%200-.3%200-.2.1zm.3-2.3v.1l.1.1v-.2zm.1%201.8-.1-.2.1.2zm4-3.8.1-.1h-.1zM40.6%2045c0-.2-.2-.1-.2-.2%200%20.1%200%20.2.2.1zm.9%201.1s0-.2-.2-.2c0%20.1%200%20.2.2.2zm-3%201.7v.2c.1%200%20.1-.1%200-.2zm4.5-6-.2.2q.2%200%20.2-.2zm6.5-.8q0%20.1.2%200s-.1-.1-.2%200zm2%20.4v.2h.1v-.2h-.1zm.3-.4.1-.2s-.2%200-.1.1zm-10.2%203.2h-.1.1zm-.3.1V44h-.1v.2zm1.1%202.8h.2l-.1-.1-.1.1zm7.7-6.3h.2-.1zm-1.2%206.6h.1l-.2-.2v.2zm-7.6-2.2v.1h.1v-.1h-.1zm-3.2%202.2h.2-.2zm11.1-2.1H49zm.2.2v.1zm-2.3-2.7.1.1q0-.1%200%200zm-2.5%204.7h.1zm-6.2-3.1h-.2l.1.1v-.1zm1.3-.4v.1-.1zM50%2049.2v.1h.1v-.1zm3.4-13.9c0%20.2%200%20.5.3.5h.6l-.1-.5-.1-.2a.5.5%200%200%200-.7%200v.2zM52%2037.1v.1c-.3.1-.3.4-.3.5v.3c.2%200%20.2.3.3.4.2-.1.5-.4.5-.6s0-.4-.3-.5l-.2-.1zm.2-3.8.2.2.8-.2c-.3%200-.3-.3-.3-.4s0-.2-.2-.2h-.6v.6z%22%2F%3E%3Cpath%20d%3D%22M45%2049c0-.2%200-.4-.2-.4h1v-.1l.2.1c0-.2.3%200%20.4-.2%200-.3-.2-.4-.3-.6v-.5l.2-.2.2-.3-.2-.2h.2c.1-.3-.1-.3-.2-.5H46v-.3h.1c0%20.2.1.2.2.2h.2c0-.2.1-.3.2-.3q.2-.2%200-.2v.1l-.2-.1v-.1l-.2-.1h-.1L46%2045h-.2l-.2-.1-.2.1v.4l.2.1.2.1h-.3c-.3.1-.5.3-.5.6h-.5c.1-.2.3%200%20.4-.1.2-.2%200-.2%200-.4l.2-.4v-.2h.1c0-.2.2-.2.3-.3.1%200%20.3%200%20.3-.2V44c.1%200%20.1-.1%200-.2h-.2l-.5-.1-.3.3c0%20.2%200%20.5-.2.6%200%20.2.1.4.4.5-.5%200-.6.3-.5.7h-.1c0%20.1-.1%200-.2%200v.3c-.3%200-.4%200-.5.2v.3l.1.1c-.4.2-.4.5-.4.7h-.5s-.2%200-.3.2c0%20.2.1.3.3.3v.2c.2-.1.3%200%20.4%200%200%20.2-.1.3-.3.3l-.3.2H42v-.2h.2v-.5c.2%200%20.2-.2.1-.4v-.2l-.3-.1c-.2-.2-.3-.1-.4%200v.1c-.3%200-.3.2-.3.3H41v.2l-.1.2-.2.3.4.3-.1.1-.3-.1-.2-.1-.3.1c-.1.1-.2.2-.3%200%20.1-.2%200-.4-.1-.7v-.5c-.1-.2-.4-.1-.5-.2h-.1c-.2%200-.2.2-.2.3-.1.2-.1.3%200%20.4v.4c-.1.2%200%20.5.2.5l.3.1v.1H41q.3%200%20.3-.3l.5-.4v.2c-.4.2-.4.2-.4.5h-.1l-.2.1h1.4v-.2c.1.2.3.2.4.1h.3l.1.2h.7v-.5h.4l-.2.5h1c0-.1%200-.2-.2-.2zm-1.5-1.3-.1-.1h.1zm2.5-.3zm-.5-1.1zm-1.2.1h.1v.2h-.2v-.2zm.2%202h.1zm-.2-.7-.4-.2c.2-.2.3%200%20.4%200V47h.1v-.2l.4.1v.1l.1.1.2.1v.2h.2l.2.2h.1v.3h.2c.1-.1.1%200%20.2%200h-1l-.1.4-.1-.3-.2-.3h-.4zm.4-7.4.4.2h.7l.3.2c.1.1.4%200%20.4-.2l.1-.4c-.1-.1-.3-.3-.5-.3%200-.5%200-.5-.4-.6l-.1.3h-.3l-.3.1h-.2c-.2%200-.3.1-.3.3v.2s0%20.2.2.2zm6.8-.7v.5l-.1.2.1.1v-.1h.1c0%20.3.2.4.4.3v-.8l.2-.3h-.7zm1.5-5c0%20.2.1.3.3.3h.3v-.4c0-.2-.2-.3-.4-.2-.2.2-.3.2-.2.3zm5.7%202.4v.4l.2.2.2-.2V37l-.4.1zm-3.2-4.7V32c-.1-.2-.2-.2-.5%200l.2.6c.2%200%20.2-.1.3-.2zm-4.7%208c.1%200%20.2-.1.2-.3h-.3v.3l-.2.4c0%20.2%200%20.2.2.3l.4-.3c0-.3%200-.4-.3-.4zM48.3%2038l-.2-.3c-.1-.3-.3-.3-.6-.2.1.4.4.4.8.4z%22%2F%3E%3Cpath%20d%3D%22m41.3%2046.4-.3-.2c-.2.1-.1.2-.1.4v.2h.2l.1.2v-.1l.3-.1v-.2l-.1-.3h-.1ZM54%2036.2l-.2-.2c-.3%200-.4.1-.4.3%200%200%200%20.2.2.3H53l-.6.2v.3l.1.1c0%20.2.2.2.3.3v.2l.1.2.1-.4.4-.3c-.1-.1.1%200%20.1-.2l.1-.4.3-.1.3-.1-.3-.2Zm-2.9%207.9c0-.2-.1-.2-.2-.2-.2%200-.2.2-.2.3v.2c.3.1.3-.2.4-.3Zm7.1-11%20.2.2h.3V33c-.3-.2-.4-.2-.5.1Zm-11.5%206.6c.1%200%20.2-.2.1-.3%200-.1-.1-.2-.2-.1-.2%200-.3.2-.2.3h.3ZM52%2037v-.3q-.2-.2-.4-.1c0%20.2%200%20.4.4.4Zm.6%206.3V43c-.2%200-.3.1-.4.3.2.1.3.1.4%200Zm2.4-4c.2%200%20.4.2.5%200l-.3-.3-.3.3Zm.3-5c.2.2.3.1.4-.2-.2-.2-.2-.2-.4.2Zm-9.8%206.3.1.4h.2c0-.3%200-.4-.3-.4Z%22%2F%3E%3Cpath%20d%3D%22M58.7%2033.5v.2h-.1v-.2l-.1-.2-.2.1-.2.1h-.5v.2l-.2.1-.1.2H57v.4h.1l.2.2.1.1c.1.2.2.2.4.2h.2l-.3.1-.2.1c-.1%200-.3%200-.3.2v.5h-.4v.2h.1c.2%200%20.3%200%20.3-.2%200%20.3.2.4.5.4h.1l.3.1c0%20.2.2.3.3.4v-.2h.6v-2h-.2l-.1.3c-.1%200-.2%200-.2.2h-.2v-.2l.2-.3.2-.3v-.3h.3c-.1-.4-.2-.4-.4-.4Zm-.2%202.1ZM49%2040.8h-.3l-.2.2.3.2v.1c.1%200%20.3%200%20.2-.1V41c.2%200%20.2%200%20.3-.2l-.1-.2c-.2%200-.3.1-.3.2Zm7.8-9.5-.3-.1h-.2v.2h.3l.2-.1ZM42.4%2048.5h.3l.2-.1-.2-.2c-.2%200-.3.1-.3.3Zm14.1-15.1.1.3.2-.1v-.3h-.3Zm-.1.6.2.1s.1-.2%200-.4l-.2.3Zm-6.6%2015.2c0-.1%200-.1-.1%200h-.1.2Zm5-14.2c0-.1%200%200-.1%200h-.2v.1l.3.1V35Zm-9.2%2013.7.2.2c.1%200%200-.1%200-.1%200-.1%200-.2-.2-.1Zm4.4-8.4h-.2c0%20.1%200%20.2.1.1h.1Zm1-2.9q0-.2-.2-.3l.1.3Zm-3.5%206.8v-.3.3ZM59%2037.7v-.2.2Zm-11%203.6V41v.1Zm7.7%202.6v.2-.2Zm-8.9%203.3v.1-.1Zm6-4.7a2%202%200%200%201-.2%200h.2Zm1-.1c.1.1.2%200%20.2%200h-.2ZM59%2031.6v.2-.2ZM47.6%2046.4h-.1c0%20.1%200%200%20.1%200ZM58.9%2033v.2-.2Zm-.7-3h.1v-.1ZM45.4%2041.2h.1V41Zm10.8-5.4-.1.1h.1v-.1ZM48.5%2048c-.1%200-.1.1%200%20.1Zm1.5-6.7h.2-.2Zm3.9-3.8zm2.4-7.9-.2.1c-.2%200-.2.2-.3.3v.2l.2.2.1.1c.3.1.5.2.7%200l.1-.1h.4c.2%200%20.3-.2.3-.3v-.5h-.7c-.2-.5-.2-.5-.6-.4v.4Zm1.4%202.7.1-.3v-.1h-.4c-.1%200-.3.2-.2.3l-.1-.1-.1-.1h-.3c-.2-.1-.4%200-.5.2v.5h.2l.2.1.4.2.2.4c0%20.1.2.2.3.1.1%200%200-.1%200-.2l-.1-.4v-.4h.1c.2%200%200%20.2.1.4s.1.2.2.1h.2c-.1-.2-.1-.2%200-.4l-.3-.3Zm.6-.3v.7h.4c.1%200%20.2%200%20.2-.2l.1-.3v-.1c0-.2-.1-.4-.4-.4h-.4v.3Zm.5-5.2-.4.1v.5h.1l.4.3.2-.3V27h-.3Zm-.2%201.2c0%20.3%200%20.5.3.5h.2V28c-.2-.1-.3-.2-.5%200ZM56%2029h.4v-.3c0-.2-.2-.3-.4-.3h-.3l.1.4.2.1Zm2.6%202.1v.4h.5V31c-.2-.2-.4-.1-.5%200Zm-.6-4.9-.4-.4c-.3%200-.4.1-.4.4l.4.2q.2%200%20.3-.2Zm-7.2%2010.3c-.2%200-.3.1-.3.3l.2.2c.3-.2.2-.4.1-.5Zm1.9-.8h.2c-.1-.2-.3-.2-.5-.2%200%200-.2%200-.2.2.1.1.1.1.4%200h.1Zm3.5-.2H56l-.2.2h.7s.1-.2%200-.2c0-.1-.1-.2-.2-.1v.1Zm2.2-11.1-.1-.3c-.2%200-.1.2-.3.2v.1c.2.2.3.1.4%200Zm-.8%203.4h-.2q.2.3.4.2c0-.1%200-.2-.2-.3Zm-2.1%2016.6zm-.7-6.4h.2v-.2l-.3.1Zm-2.4.6.1.2q.2-.1.2-.4c-.2%200-.2%200-.3.2Zm3.9-3.8v-.3c-.2%200-.3%200-.3.2l.1.1h.2Zm1.9-6.6V28c-.2%200-.2%200-.2.2h.2ZM56.4%2044v.1h.3v-.2h-.3ZM59%2030.7v-.1h-.2l.1.1Zm-5%205.9s.2.2.3%200H54Zm1.5.7s0-.1-.2%200h.2Zm-.5-4.5v.2-.2Zm-.3%202.7v.1h.2-.2Zm-.1.3-.1-.2v.1Zm.5.8H55s.1%200%200%200Zm-1.8%203.3h-.2v.1l.2-.1Zm-.3-3.7h.1Z%22%2F%3E%3C%2Fg%3E%3Cpath%20fill%3D%22%231d3ba9%22%20d%3D%22M16.6%2011.2h3.7V8.6c0-.8-3.7-.8-3.7%200v2.6ZM8.7%2034.5h19.5c1.7%200%201.7-11.4%200-11.4H8.7c-1.6%200-1.6%2011.4%200%2011.4Z%22%2F%3E%3Cg%20fill%3D%22%230c2b77%22%3E%3Cpath%20d%3D%22M25.7%2016v35.2H11.3V16c0-3.4%202.7-6.2%206.1-6.2h2.1c3.4%200%206.2%202.8%206.2%206.2Z%22%2F%3E%3Crect%20width%3D%2217.3%22%20height%3D%224%22%20x%3D%229.8%22%20y%3D%2216.2%22%20rx%3D%22.7%22%20transform%3D%22rotate%28180%2018.5%2018.2%29%22%2F%3E%3C%2Fg%3E%3Cg%20fill%3D%22%231d3ba9%22%3E%3Cpath%20d%3D%22M27.1%2017H9.8c0-.4.4-.7.8-.7h15.8c.4%200%20.7.3.7.7v.2Z%22%2F%3E%3Crect%20width%3D%223.4%22%20height%3D%223.4%22%20x%3D%2216.8%22%20y%3D%2227%22%20rx%3D%22.6%22%20transform%3D%22rotate%28225%2018.5%2028.7%29%22%2F%3E%3Cpath%20d%3D%22M19.5%2040.3v10.9h-2v-11c0-.4.3-.8.8-.8h.3c.5%200%201%20.4%201%20.9Zm4.1%200v10.9h-2.1v-11c0-.4.4-.8.9-.8h.3c.5%200%201%20.4%201%20.9Zm-8.2%200v10.9h-2v-11c0-.4.3-.8.8-.8h.3c.5%200%201%20.4%201%20.9Z%22%2F%3E%3C%2Fg%3E%3Ccircle%20cx%3D%2218.5%22%20cy%3D%2228.8%22%20r%3D%224.9%22%20fill%3D%22none%22%20stroke%3D%22%231d3ba9%22%20stroke-width%3D%221.8%22%2F%3E%3Cg%20stroke-miterlimit%3D%2210%22%3E%3Cpath%20fill%3D%22%236c27a8%22%20stroke%3D%22%236c27a8%22%20stroke-width%3D%22.4%22%20d%3D%22M59.2%2058.8h-58V47.2h58z%22%2F%3E%3Cpath%20fill%3D%22%2347127f%22%20stroke%3D%22%239961e2%22%20stroke-width%3D%221.4%22%20d%3D%22M8.2%2059.2v-4.5c0-1.8%201.4-3.2%203.1-3.2H52c1.7%200%203%201.4%203%203.2v4.5%22%2F%3E%3C%2Fg%3E%3Cpath%20fill%3D%22%230254c2%22%20d%3D%22M58.7%201v57.7H1V1h57.6m1-1.1H0v59.7h59.7V0Z%22%2F%3E%3C%2Fsvg%3E";

var badFly = "data:image/png;base64,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";

var celebrate = "../static/celebrate-ece5a54e321ab2e7.png";

var hover = "../static/hover-13bd4972c72e1a52.gif";

var spotlight = "data:image/gif;base64,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";

var badCard = "data:image/png;base64,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";

var castle = "../static/castle-7575ab637e5138e2.svg";

var fourSquares = "../static/fourSquares-de5c55d13d7de923.png";

var goodCard = "data:image/png;base64,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";

var hydrant = "../static/hydrant-d11f08c8f1a631a3.svg";

var iconBad = "data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20id%3D%22Layer_2%22%20data-name%3D%22Layer%202%22%20viewBox%3D%220%200%2016.98%2015.78%22%3E%3Cdefs%3E%3Cstyle%3E.cls-1%7Bfill%3A%235eccbe%7D%3C%2Fstyle%3E%3C%2Fdefs%3E%3Cg%20id%3D%22Layer_2-2%22%20data-name%3D%22Layer%202%22%3E%3Cpath%20d%3D%22m12.3%205.91.05.01h.01l-.06-.02v.01z%22%20class%3D%22cls-1%22%2F%3E%3Cpath%20d%3D%22M16.89%2014.6c-.2-.49-.62-.81-.98-1.1-.18-.14-.35-.27-.48-.42-.68-1.19-.49-2.05-.27-3.03.29-1.31.62-2.79-1.16-5.15-.97-3.08-1.69-4.42-2.56-4.76-.67-.26-1.3.11-1.97.5-.91.53-1.95%201.14-3.56.74-.39-.21-.76-.26-1.08-.15-.57.19-.85.82-1.09%201.38-.12.28-.25.57-.38.71v.02c-.62.65-1.74%201.85-1.52%203.99.17%202.95%200%203.3-.6%203.93-.53.57-.41%201.2-.31%201.7.06.32.12.62.05.91-.12.49-.32.68-.54.89-.14.13-.28.27-.4.48a.34.34%200%200%200%20.3.51l16.28.03c.18%200%20.33-.13.34-.31%200-.09.05-.57-.07-.87Zm-3.9-8.41-.35-.14.34.15C11.96%208.63%2010.4%209.91%208.35%2010H8.2c-2.62%200-4.31-2.92-4.87-3.89a.497.497%200%200%201%20.06-.58c.14-.16.37-.21.57-.13.59.25%201.83.68%203.5.77l.33.02.03.33c.06.77.52%201.21.79%201.4.23-.24.64-.76.71-1.49l.03-.3.3-.03c1.66-.18%202.38-.43%202.66-.56.19-.09.41-.05.57.09.15.15.2.37.12.56ZM1.77%201.96c-.6.05-.55.82-.38%201.2%200%200%20.34.51.68.14.1-.11.17-.25.21-.4.05-.2.06-.43-.02-.62-.09-.19-.29-.34-.5-.32ZM2.78.9c.04.26.17.61.39.68.22.07.44-.21.46-.6.03-.39-.14-.95-.49-.97-.38-.03-.42.52-.36.89ZM14.12.05c-.6.05-.55.82-.38%201.2%200%200%20.34.51.68.14.1-.11.17-.25.21-.4.05-.2.06-.43-.02-.62-.09-.19-.29-.34-.5-.32ZM15.8%202.2c-.21-.2-.42-.2-.6-.09-.37.22-.65.85-.66%201.15-.01.37.13.88.71.79.54-.08.92-1.49.55-1.86Z%22%20class%3D%22cls-1%22%2F%3E%3C%2Fg%3E%3C%2Fsvg%3E";

var land = "data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20data-name%3D%22Layer%202%22%20viewBox%3D%220%200%201287.15%2038.21%22%3E%3Cg%20data-name%3D%22Layer%202%22%3E%3Cpath%20d%3D%22M1015.47%2032.86V16.23h6.44v16.63%22%20style%3D%22fill%3A%231d3ba9%22%2F%3E%3Cpath%20d%3D%22M1011.69%2017.09s-4.06%203.8-6.43.02c-2.37-3.79%201.02-3.57%201.02-3.57s-1.61-3.51.42-5.8%203.64-1.27%203.64-1.27-.76-3.81.93-4.4%203.21%201.52%203.21%201.52.68-3.93%203.3-3.57%203.05%203.66%203.05%203.66%202.37-1.95%204.06-.17%201.18%204.48%201.18%204.48%201.61-3.14%203.89-2.25%201.52%203.09%201.52%203.09%202.37%201.5%201.1%203.03-3.64%202.39-3.64%202.39%203.3.79%202.45%202.67-3.81%201.85-3.81%201.85l-2.37%201.14h-8.12s-3.38%201.43-4.23.5-1.18-3.34-1.18-3.34Z%22%20style%3D%22fill%3A%234db6ac%22%2F%3E%3Cpath%20d%3D%22M0%2038.21V8.39c11.13%201.08%2065.43%2017.4%2086.67%2016.08s47.4%205.28%2054%207.49%2030.36-4.19%2053.46-11.1S313.6%2031.73%20343.3%2031.95s28.38-5.5%2043.56-8.34%2057.42%205.47%2079.86%206.02%2059.14-6.02%2059.14-6.02c19.73-3.77%2032.73-14.57%2048.01-12.14s28.59%205.33%2042.72%205.86%2045.82-3.34%2053.74-5.86%2035.64-5.4%2043.56%200%2018.15%202.39%2035.64%2014.17c7.45%205.02%2034.65%206.35%2042.57%207.54s64.02.3%2069.3-1.24%2034.72-6.47%2043.1-5.98%2092.86%204.88%20107.39%205.98%2066.66-2.03%2089.76-2.12%2046.2-.31%2059.4%202.12c10.51%201.93%2025.61-.92%2036.33-2.2%201.3-.16%202.53-.35%203.69-.39%2033.98-1.17%2041.27%207.55%2049%204.27s13.53-7.51%2037.04-9.16V38.2H0Z%22%20style%3D%22fill%3A%230c2b77%22%2F%3E%3C%2Fg%3E%3C%2Fsvg%3E";

var logo = "data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20xml%3Aspace%3D%22preserve%22%20style%3D%22enable-background%3Anew%200%200%20382.4%20381.2%22%20viewBox%3D%220%200%20382.4%20381.2%22%3E%3Cpath%20d%3D%22M198.4%200c2.4.2%204.9.4%207.3.6%2027%202%2052.4%209.5%2076.3%2022.3%2016.2%208.7%2030.8%2019.6%2043.9%2032.5%204.1%204.1%207.9%208.5%2011.7%2012.8%201.7%201.9%201.7%202%203.5.2l39.1-39.1c.5-.5%201-1%201.5-1.4.1%200%20.3.1.5.2v151.7c0%202.8.2%205.6.2%208.3%200%202.6%200%202.6-2.6%202.6l-56-.3c-31.9%200-63.8%200-95.6.1-2.5%200-5%20.1-7.5.2-.4%200-.8-.1-1.6-.2l1.7-1.7c15.5-15.5%2030.9-31%2046.4-46.4%201.1-1.1%201.2-1.9.3-3.2-15.6-22.4-36.9-36-64-40-3.8-.6-7.6-1.1-11.4-1.6-1.6-.2-2.1.4-2.1%202%20.1%2016.3.1%2032.5.1%2048.8%200%204.2.1%208.4.2%2012.6%200%20.6-.1%201.2-.1%202.2-.8-.7-1.4-1.2-1.8-1.6l-46.3-46.3c-1.2-1.2-1.9-1.3-3.3-.3-22.5%2015.6-35.9%2036.9-40.1%2064l-1.5%209.9c-.3%202.1-.1%202.3%202%202.3%2020.3%200%2040.6%200%2060.8-.1h2.8c-.8%201-1.3%201.6-1.8%202.1-15.4%2015.4-30.7%2030.7-46.1%2046-1.3%201.3-1.3%202.1-.3%203.6%2015.3%2021.9%2036.1%2035.3%2062.5%2039.6%206%201%2012%202%2018.2%201.7%2017.5-.9%2033.7-5.7%2047.8-16.4%204.6-3.5%209.1-7%2013.2-10.9%206.1-5.8%2011.1-12.5%2015.3-19.9.2-.4.4-.8.7-1.1.1-.1.2-.3.4-.6.6.5%201.1.9%201.6%201.3%2013.4%2013.5%2026.8%2027%2040.1%2040.5%209%209.1%2018%2018.3%2027.1%2027.3%201.2%201.2%201.2%202%20.2%203.3-12.5%2015.9-27%2029.6-43.7%2040.9-19.2%2013.1-40.1%2022.3-62.7%2027.7-9.6%202.3-19.2%204-29.1%204.5-7%20.4-14.1.8-21.1.6-16.4-.4-32.6-3-48.4-7.7-18-5.3-34.8-13.2-50.4-23.4-2.5-1.6-4.9-3.5-7.4-5.1-10.2-6.4-18.7-14.7-27-23.3-3.1-3.2-6-6.7-9.2-10.3L.4%20353.8c-.1-1.3-.1-2-.1-2.8V199.9c0-4.9-.1-9.8%200-14.6.3-16.4%203-32.5%207.6-48.2%205.5-18.9%2013.9-36.5%2024.9-52.8%208.4-12.4%2018.1-23.6%2029.1-33.8%202-1.9%204.1-3.6%206.2-5.3.7-.6%201.4-1.2%202.2-2C55.7%2029%2041.7%2014.9%2027.7.9c0-.1.1-.3.1-.4.7-.1%201.4-.1%202.2-.1h150.8c1%200%202-.2%203-.3%204.8-.1%209.7-.1%2014.6-.1z%22%20style%3D%22fill%3A%23020612%22%2F%3E%3C%2Fsvg%3E";

var logoBlue = "data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20xml%3Aspace%3D%22preserve%22%20style%3D%22enable-background%3Anew%200%200%20382.4%20381.2%22%20viewBox%3D%220%200%20382.4%20381.2%22%3E%3Cpath%20d%3D%22M198.4%200c2.4.2%204.9.4%207.3.6%2027%202%2052.4%209.5%2076.3%2022.3%2016.2%208.7%2030.8%2019.6%2043.9%2032.5%204.1%204.1%207.9%208.5%2011.7%2012.8%201.7%201.9%201.7%202%203.5.2l39.1-39.1c.5-.5%201-1%201.5-1.4.1%200%20.3.1.5.2v151.7c0%202.8.2%205.6.2%208.3%200%202.6%200%202.6-2.6%202.6l-56-.3c-31.9%200-63.8%200-95.6.1-2.5%200-5%20.1-7.5.2-.4%200-.8-.1-1.6-.2l1.7-1.7c15.5-15.5%2030.9-31%2046.4-46.4%201.1-1.1%201.2-1.9.3-3.2-15.6-22.4-36.9-36-64-40-3.8-.6-7.6-1.1-11.4-1.6-1.6-.2-2.1.4-2.1%202%20.1%2016.3.1%2032.5.1%2048.8%200%204.2.1%208.4.2%2012.6%200%20.6-.1%201.2-.1%202.2-.8-.7-1.4-1.2-1.8-1.6l-46.3-46.3c-1.2-1.2-1.9-1.3-3.3-.3-22.5%2015.6-35.9%2036.9-40.1%2064l-1.5%209.9c-.3%202.1-.1%202.3%202%202.3%2020.3%200%2040.6%200%2060.8-.1h2.8c-.8%201-1.3%201.6-1.8%202.1-15.4%2015.4-30.7%2030.7-46.1%2046-1.3%201.3-1.3%202.1-.3%203.6%2015.3%2021.9%2036.1%2035.3%2062.5%2039.6%206%201%2012%202%2018.2%201.7%2017.5-.9%2033.7-5.7%2047.8-16.4%204.6-3.5%209.1-7%2013.2-10.9%206.1-5.8%2011.1-12.5%2015.3-19.9.2-.4.4-.8.7-1.1.1-.1.2-.3.4-.6.6.5%201.1.9%201.6%201.3%2013.4%2013.5%2026.8%2027%2040.1%2040.5%209%209.1%2018%2018.3%2027.1%2027.3%201.2%201.2%201.2%202%20.2%203.3-12.5%2015.9-27%2029.6-43.7%2040.9-19.2%2013.1-40.1%2022.3-62.7%2027.7-9.6%202.3-19.2%204-29.1%204.5-7%20.4-14.1.8-21.1.6-16.4-.4-32.6-3-48.4-7.7-18-5.3-34.8-13.2-50.4-23.4-2.5-1.6-4.9-3.5-7.4-5.1-10.2-6.4-18.7-14.7-27-23.3-3.1-3.2-6-6.7-9.2-10.3L.4%20353.8c-.1-1.3-.1-2-.1-2.8V199.9c0-4.9-.1-9.8%200-14.6.3-16.4%203-32.5%207.6-48.2%205.5-18.9%2013.9-36.5%2024.9-52.8%208.4-12.4%2018.1-23.6%2029.1-33.8%202-1.9%204.1-3.6%206.2-5.3.7-.6%201.4-1.2%202.2-2C55.7%2029%2041.7%2014.9%2027.7.9c0-.1.1-.3.1-.4.7-.1%201.4-.1%202.2-.1h150.8c1%200%202-.2%203-.3%204.8-.1%209.7-.1%2014.6-.1z%22%20style%3D%22fill%3A%23448aff%22%2F%3E%3C%2Fsvg%3E";

var noClick = "data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20xml%3Aspace%3D%22preserve%22%20id%3D%22Layer_1%22%20x%3D%220%22%20y%3D%220%22%20style%3D%22enable-background%3Anew%200%200%2048%2048%22%20version%3D%221.1%22%20viewBox%3D%220%200%2048%2048%22%3E%3Cstyle%3E.st0%7Bfill%3A%23ee0290%7D%3C%2Fstyle%3E%3Cpath%20d%3D%22M31%2025.5c.7-2.4%201.5-4.9%202.2-7.3.6-1.9-.3-2.9-2.2-2.3-2.5.7-4.9%201.5-7.4%202.2l7.4%207.4zM25.2%2024l-5-5c-2.1.6-4.2%201.3-6.3%201.9-.8.2-1.7.6-1.4%201.6.2.6.9%201.3%201.5%201.5.7.3%201.3.5%202.1.8.9.3%201.2%201.5.5%202.2-2.1%202.1-4.2%204.1-6.2%206.3-1.3%201.4-1.5%203.1-.7%204.7.8%201.4%202.3%202.2%204.1%201.8.9-.2%201.7-.8%202.4-1.4%202-1.9%203.9-3.8%205.9-5.8.7-.7%201.8-.4%202.2.5.2.7.5%201.4.8%202.1.3.6.9%201.4%201.5%201.5%201%20.2%201.4-.7%201.6-1.6.6-2.1%201.2-4.2%201.9-6.3L25.2%2024z%22%20class%3D%22st0%22%2F%3E%3Cpath%20d%3D%22M23.1%2026.1%204.5%207.6c-.6-.6-.6-1.6%200-2.2.6-.6%201.5-.6%202.1%200L43.2%2042c.6.6.6%201.5%200%202.1-.6.6-1.5.6-2.1%200l-13-13-5-5z%22%20class%3D%22st0%22%2F%3E%3C%2Fsvg%3E";

var pointer = "data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2049.48%2049.48%22%3E%3Cpath%20d%3D%22M23.05%2049.48v-4.24c-5.16-.53-9.45-2.5-12.88-5.93-3.43-3.43-5.4-7.72-5.93-12.88H0v-3.39h4.24c.53-5.16%202.5-9.45%205.93-12.88%203.43-3.43%207.72-5.4%2012.88-5.93V0h3.39v4.24c5.16.53%209.45%202.5%2012.88%205.93%203.43%203.43%205.4%207.72%205.93%2012.88h4.24v3.39h-4.24c-.53%205.16-2.5%209.45-5.93%2012.88-3.43%203.43-7.72%205.4-12.88%205.93v4.24h-3.39Zm1.69-7.57c4.71%200%208.75-1.69%2012.12-5.06%203.37-3.37%205.06-7.41%205.06-12.12%200-4.71-1.69-8.75-5.06-12.12-3.37-3.37-7.41-5.06-12.12-5.06s-8.75%201.69-12.12%205.06-5.06%207.41-5.06%2012.12c0%204.71%201.69%208.75%205.06%2012.12%203.37%203.37%207.41%205.06%2012.12%205.06Z%22%20style%3D%22fill%3A%23ee0290%22%2F%3E%3C%2Fsvg%3E";

var gameHTML = x`
  <div id="game" class="l0">
    <div class="overlay" id="overlay"></div>
    <div class="castle-wrap">
      <img src="${land}" class="land" alt="" />
      <img src="${castle}" class="castle" alt="" id="castle" />
    </div>
  </div>
  <div class="globalnav">
    <mwc-icon-button
      aria-controls="sitemap"
      aria-expanded="true"
      aria-label="Close"
      class="closebtn"
      icon="close"
      id="closegame"
    ></mwc-icon-button>
  </div>
  <div class="controller">
    <ul>
      <!-- 
        <li class="status-container">
          <h3 class="bold">status:</h3> <span id="status">Game hasn't started</span>
        </li>
      -->
      <li class="status-container score-wrap" id="statuscontainer">
        <div class="score-container bad-score score-container">
          <h3>
            <img src="${iconBad}" alt="Bads caught" />
            <span id="badscore" class="score">0</span>
          </h3>
          <span class="badge">👀 That's a lot of bads</span>
        </div>
        <div class="human-score-container score-container">
          <h3>
            <i class="material-symbols-rounded" alt="Humans saved">face</i>
          </h3>
          <span id="humanscore" class="score">0</span>
          <span class="badge">👏 Way to save the humans!</span>
        </div>
        <div class="high-score-container score-container">
          <h3 class="bold">
            <i class="material-symbols-rounded" alt="High score"
              >military_tech</i
            >
          </h3>
          <span id="highscore" class="score">0</span>
          <span class="badge">🎉 New High Score</span>
        </div>
        <div class="bonus-container score-container" id="bonusscorewrap">
          <h3 class="bold">
            <i class="material-symbols-rounded" alt="Items">add</i>
          </h3>
          <span id="bonuses" class="bonusicons"> </span>
          <span class="badge">🎉 all badges collected</span>
        </div>
      </li>

      <li class="reload-container ready">
        <span class="progress-wrap">
          <h3><img src="${logo}" alt="" /></h3>
          <progress id="progress" class="progress" value="100" max="100">
            100%
          </progress>
          <span class="text">
            <span class="icon"><span class="key">R</span></span>
          </span>
        </span>
      </li>
    </ul>
    <div class="intro">
      <div class="intro-wrap">
        <h1>BadFinder</h1>
        <div class="content">
          <div class="content-wrap">
            <img src="${badCard}" alt="" />
            <span>
              <img src="${pointer}" class="norm" alt="don't click" />
              <span>Get the bads before they reach the castle.</span>
            </span>
          </div>
          <div class="content-wrap">
            <img src="${goodCard}" alt="" />
            <span>
              <img src="${noClick}" class="norm" alt="don't click" />
              <span>Protect the humans!</span>
            </span>
          </div>
        </div>
        <button id="start" class="play">Play</button>
      </div>
    </div>
  </div>

  <div class="bonusdialogue" id="dialoguebonus">
    <div class="bonusdialogue-wrap">
      <div class="content">
        <img src="${fourSquares}" alt="" class="featuredimg" id="bonusimg" />
        <div>
          <h4>Items unlocked!</h4>
          <p>Collect squares with bikes, crosswalks and hydrants.</p>
        </div>
      </div>
      <button id="resume">Let's go</button>
    </div>
  </div>

  <div class="bonusdialogue" id="dialoguescan">
    <div class="bonusdialogue-wrap">
      <div class="content">
        <div class="instructions-wrap">
          <span class="key">R</span>
          <span>=</span>
          <img src="${logoBlue}" alt="" />
        </div>
        <div>
          <p>
            Blocks are now hidden, Press the R key to run a reCAPTCHA and reveal
            them.
          </p>
          <!--Todo: change to "tap recaptcha" on mobile -->
        </div>
      </div>
      <button id="resume">Play on</button>
    </div>
  </div>

  <div class="bonusdialogue fail" id="dialoguefail">
    <div class="bonusdialogue-wrap">
      <div class="content">
        <img src="${badFly}" alt="" class="featuredimg" id="levelupimg" />
        <!-- Change from bad-fly  -->
        <div>
          <h4><span id="badcount">14</span> bads caught!</h4>
          <p>
            <span id="reason">A bad slipped by and got to the castle.</span>
            That's okay, you <span id="humancount">still saved 4 humans.</span>
          </p>
        </div>
        <div class="levelup-container" id="levelupcontainer">
          <img src="${hover}" alt="" />
          <div>
            <h5>Expert mode!</h5>
            <p id="levelupdesc">
              Hovering on a square now reveals the entire thing!
            </p>
          </div>
        </div>
        <button id="restart">Keep playing</button>
      </div>
    </div>
  </div>

  <div class="dialogue" id="dialoguenewlevel">
    <p class="reason" id="reason">Nice try</p>
    <div class="levelup-container" id="levelupcontainer">
      <img src="${hydrant}" alt="" id="bonusimg" />
      <p>
        You've unlocked items! Click on squares with bikes, crosswalks and
        hydrants to collect them all.
      </p>
    </div>
    <button class="startgame icon-btn" id="restart">
      <i class="material-symbols-rounded">play_arrow</i>
    </button>
  </div>

  <svg
    id="boomboom"
    class="boomboom"
    data-name="Layer 2"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 99.1 89.19"
  >
    <defs>
      <style>
        .cls-1 {
          fill: #fbfd17;
        }

        .cls-2 {
          fill: #9b9a9f;
        }
      </style>
    </defs>
    <g>
      <g id="right" class="right">
        <circle class="cls-2" cx="81.83" cy="22.19" r="5.92" />
        <circle class="cls-2" cx="63.11" cy="31.69" r="1.04" />
        <circle class="cls-2" cx="68.29" cy="47.7" r="1.04" />
        <circle class="cls-2" cx="80.79" cy="51.86" r="1.04" />
        <circle class="cls-2" cx="81.83" cy="40.31" r="4.16" />
        <circle class="cls-2" cx="75.92" cy="48.74" r="4.16" />
        <circle class="cls-2" cx="67.64" cy="43.95" r="4.16" />
        <circle class="cls-2" cx="60" cy="41.04" r="4.16" />
        <circle class="cls-2" cx="74.86" cy="32.72" r="6.75" />
        <circle class="cls-2" cx="57.63" cy="36.15" r="6.75" />
        <circle class="cls-2" cx="87.75" cy="32.72" r="3.1" />
        <circle class="cls-2" cx="71.7" cy="40" r="3.1" />
        <circle class="cls-2" cx="57.92" cy="51.86" r="4.16" />
        <circle class="cls-2" cx="63.49" cy="49.8" r="5.86" />
        <circle class="cls-2" cx="53.76" cy="62.27" r="6.97" />
        <circle class="cls-2" cx="81.83" cy="59.87" r="6.97" />
        <circle class="cls-2" cx="71.7" cy="58.12" r="4.16" />
      </g>
      <g id="bottom" class="bottom">
        <circle class="cls-2" cx="41.29" cy="68.21" r="1.04" />
        <circle class="cls-2" cx="57.92" cy="75.8" r="3.1" />
        <circle class="cls-2" cx="35.19" cy="74.81" r="3.1" />
        <circle class="cls-2" cx="68.29" cy="69.24" r="3.1" />
        <circle class="cls-2" cx="47.5" cy="74.81" r="4.16" />
        <circle class="cls-2" cx="42.33" cy="61.6" r="6.75" />
        <circle class="cls-2" cx="44.4" cy="58.12" r="3.1" />
      </g>
      <g id="left" class="left">
        <circle class="cls-2" cx="24.58" cy="22.19" r="4.16" />
        <circle class="cls-2" cx="15.42" cy="24.05" r="1.04" />
        <circle class="cls-2" cx="32.09" cy="62.93" r="1.04" />
        <circle class="cls-2" cx="16.46" cy="64.74" r="3.1" />
        <circle class="cls-2" cx="23.53" cy="30.5" r="4.16" />
        <circle class="cls-2" cx="28.74" cy="30.65" r="1.04" />
        <circle class="cls-2" cx="13.35" cy="42.08" r="1.04" />
        <circle class="cls-2" cx="37.05" cy="41.04" r="1.04" />
        <circle class="cls-2" cx="32.89" cy="53.96" r="4.16" />
        <circle class="cls-2" cx="20.03" cy="50.8" r="5.09" />
        <circle class="cls-2" cx="32.54" cy="36.89" r="5.09" />
        <circle class="cls-2" cx="44.4" cy="47.7" r="4.16" />
        <circle class="cls-2" cx="26.63" cy="40.31" r="5.72" />
        <circle class="cls-2" cx="44.1" cy="33.69" r="8.67" />
        <circle class="cls-2" cx="31.05" cy="26.34" r="5.72" />
        <circle class="cls-2" cx="37.05" cy="45.19" r="6.75" />
        <circle class="cls-2" cx="48.55" cy="49.8" r="6.75" />
        <circle class="cls-2" cx="29.78" cy="62.93" r="6.75" />
        <circle class="cls-2" cx="23.53" cy="57.07" r="3.1" />
        <circle class="cls-2" cx="13.65" cy="47.7" r="3.1" />
        <circle class="cls-2" cx="16.84" cy="33.69" r="3.19" />
      </g>
      <g id="up" class="up">
        <circle class="cls-2" cx="69.64" cy="28.1" r="1.04" />
        <circle class="cls-2" cx="58.96" cy="12.1" r="1.04" />
        <circle class="cls-2" cx="48.04" cy="13.14" r="2.08" />
        <circle class="cls-2" cx="57.63" cy="24.05" r="5.72" />
        <circle class="cls-2" cx="37.05" cy="18.96" r="5.72" />
        <circle class="cls-2" cx="48.55" cy="22.19" r="6.75" />
        <circle class="cls-2" cx="69.64" cy="17.45" r="6.75" />
        <circle class="cls-2" cx="70.67" cy="22.25" r="4.81" />
        <circle class="cls-2" cx="65.87" cy="28.1" r="4.16" />
        <circle class="cls-2" cx="64.15" cy="14.26" r="3.19" />
      </g>
      <path
        class="blob"
        d="M47.03,80.71s-4.86,9.68-16.19,8.36c-11.33-1.32-5.83-13.86-7.15-17.38S6.96,57.85,5.42,49.04-3.6,34.28,2.12,29.44s10.92-2.3,12.28-1.04,5.1-6.86,7.08-9.62,9.68-7.16,13.86-8.26S47.94-3.78,60.02,1.06s9.83,13.52,11.72,16.55,12.01-3.35,17.07-3.13c5.06,.22,11.44,9.02,10.12,14.96s-.88,23.38-5.06,27.2c-4.18,3.82-10.48,15.92-23.17,20.32l-12.69,4.4s-7.22-1.1-10.98-.66Z"
      />
    </g>
  </svg>

  <svg
    class="crackin"
    id="crackin"
    data-name="Layer 2"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 55.12 55.12"
  >
    <defs>
      <style>
        .cls-1 {
          fill: #9b9a9f;
        }
      </style>
    </defs>
    <g id="rect">
      <g id="right" class="right">
        <polygon
          class="cls-1"
          points="51.17 55.12 54.71 55.12 53.81 51.4 51.17 55.12"
        />
        <polygon
          class="cls-1"
          points="54.71 55.12 55.12 55.12 55.12 49.56 53.81 51.4 54.71 55.12"
        />
        <polygon
          class="cls-1"
          points="53.81 51.4 48.51 29.4 34.92 34.17 42.86 55.12 51.17 55.12 53.81 51.4"
        />
        <polygon
          class="cls-1"
          points="53.81 51.4 55.12 49.56 55.12 27.08 48.51 29.4 53.81 51.4"
        />
        <polygon
          class="cls-1"
          points="32.02 26.51 34.92 34.17 48.51 29.4 45.21 15.7 32.02 26.51"
        />
        <polygon
          class="cls-1"
          points="48.51 29.4 55.12 27.08 55.12 7.59 45.21 15.7 48.51 29.4"
        />
      </g>
      <g id="bottom" class="bottom">
        <polygon
          class="cls-1"
          points="12.68 49.65 15.4 55.12 21.98 55.12 23.24 43.28 12.68 49.65"
        />
        <polygon
          class="cls-1"
          points="23.8 38.08 23.24 43.28 35.56 35.86 23.24 43.28 21.98 55.12 42.86 55.12 34.92 34.17 23.8 38.08"
        />
        <polygon
          class="cls-1"
          points="12.68 49.65 23.24 43.28 23.8 38.08 9.44 43.12 12.68 49.65"
        />
        <polygon
          class="cls-1"
          points="32.02 26.51 32.02 26.51 26.56 12.1 26.56 12.3 23.8 38.08 34.92 34.17 32.02 26.51 32.02 26.51"
        />
      </g>
      <g id="top" class="top">
        <polygon
          class="cls-1"
          points="45.21 15.7 42.58 4.79 30.84 5.54 29.54 7.53 40.15 19.84 29.54 7.53 26.56 12.1 32.02 26.51 45.21 15.7"
        />
        <polygon
          class="cls-1"
          points="27.99 5.73 29.54 7.53 30.84 5.54 27.99 5.73"
        />
        <polygon
          class="cls-1"
          points="45.21 15.7 55.12 7.59 55.12 3.98 42.58 4.79 45.21 15.7"
        />
        <polygon
          class="cls-1"
          points="9.45 6.92 14.36 0 10.74 0 3.42 7.31 9.45 6.92"
        />
        <polygon
          class="cls-1"
          points="27.99 5.73 23.05 0 14.36 0 9.45 6.92 27.99 5.73"
        />
        <polygon
          class="cls-1"
          points="42.58 4.79 41.42 0 34.45 0 30.84 5.54 42.58 4.79"
        />
        <polygon
          class="cls-1"
          points="55.12 3.98 55.12 0 41.42 0 42.58 4.79 55.12 3.98"
        />
        <polygon
          class="cls-1"
          points="30.84 5.54 34.45 0 23.05 0 27.99 5.73 30.84 5.54"
        />
        <polygon class="cls-1" points="10.74 0 0 0 0 7.53 3.42 7.31 10.74 0" />
      </g>
      <g id="left" class="left">
        <polygon
          class="cls-1"
          points="9.44 43.12 0 46.44 0 55.12 3.61 55.12 12.68 49.65 9.44 43.12"
        />
        <polygon
          class="cls-1"
          points="3.61 55.12 15.4 55.12 12.68 49.65 3.61 55.12"
        />
        <polygon
          class="cls-1"
          points="5.95 36.12 0 40.69 0 46.44 9.44 43.12 5.95 36.12"
        />
        <polygon class="cls-1" points="0 24.15 0 40.69 5.95 36.12 0 24.15" />
        <polygon
          class="cls-1"
          points="25.61 21.05 5.95 36.12 9.44 43.12 23.8 38.08 26.56 12.3 26.56 12.1 29.54 7.53 27.99 5.73 9.45 6.92 0 20.24 0 24.15 5.95 36.12 25.61 21.05"
        />
        <polygon
          class="cls-1"
          points="3.42 7.31 0 10.74 0 20.24 9.45 6.92 3.42 7.31"
        />
        <polygon class="cls-1" points="0 7.53 0 10.74 3.42 7.31 0 7.53" />
      </g>
    </g>
  </svg>

  <svg
    id="squarecrack"
    class="squarecrack"
    data-name="Layer 2"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 55.12 55.12"
  >
    <defs>
      <style>
        .cls-1 {
          fill: #9b9a9f;
        }
      </style>
    </defs>
    <g id="boomboom-2">
      <g id="bottom" class="bottom">
        <polygon
          class="cls-1"
          points="27.23 31.76 27.23 27.35 18.16 27.35 18.16 31.89 18.16 36.43 27.23 36.43 27.23 31.76"
        />
        <rect class="cls-1" x="18.16" y="36.43" width="9.08" height="9.08" />
        <polygon
          class="cls-1"
          points="31.76 36.43 27.23 36.43 27.23 45.51 36.31 45.51 36.31 36.43 31.76 36.43"
        />
        <rect class="cls-1" x="27.23" y="27.35" width="4.53" height="4.4" />
        <rect class="cls-1" x="27.23" y="31.76" width="4.53" height="4.67" />
        <rect class="cls-1" x="27.23" y="22.82" width="4.53" height="4.54" />
        <rect class="cls-1" x="45.39" y="45.51" width="9.32" height="9.2" />
        <rect class="cls-1" x="36.31" y="45.51" width="9.08" height="9.2" />
        <rect class="cls-1" x="18.16" y="45.51" width="9.08" height="9.2" />
        <rect class="cls-1" x="27.23" y="45.51" width="9.08" height="9.2" />
      </g>
      <g id="right" class="right">
        <polygon
          class="cls-1"
          points="31.76 27.35 31.76 31.76 31.76 36.43 36.31 36.43 45.39 36.43 48.01 36.43 48.01 29.59 48.01 22.82 40.85 22.82 40.85 22.82 40.85 22.82 31.76 22.82 31.76 27.35"
        />
        <rect class="cls-1" x="36.31" y="36.43" width="9.08" height="9.08" />
        <polygon
          class="cls-1"
          points="45.39 36.43 45.39 45.51 54.71 45.51 54.71 36.43 48.01 36.43 45.39 36.43"
        />
        <polygon
          class="cls-1"
          points="45.39 9.2 40.85 9.2 40.85 22.82 48.01 22.82 48.01 22.75 48.01 22.82 54.71 22.82 54.71 9.2 49.87 9.2 45.39 9.2"
        />
        <rect class="cls-1" x="48.01" y="22.82" width="6.7" height="6.78" />
        <rect class="cls-1" x="48.01" y="29.59" width="6.7" height="6.84" />
      </g>
      <g id="top" class="top">
        <rect class="cls-1" x="45.39" y="4.66" width="4.49" height="4.54" />
        <polygon
          class="cls-1"
          points="27.23 9.2 27.23 18.28 27.23 22.82 31.76 22.82 31.76 22.75 31.76 22.82 40.85 22.82 40.85 9.2 36.31 9.2 27.23 9.2"
        />
        <polygon
          class="cls-1"
          points="18.16 18.28 27.23 18.28 27.23 9.2 18.16 9.2 18.16 12.35 18.16 18.28"
        />
        <polygon
          class="cls-1"
          points="18.16 22.82 18.16 27.35 27.23 27.35 27.23 22.82 27.23 18.28 18.16 18.28 18.16 22.82"
        />
        <rect class="cls-1" x="49.87" width="4.83" height="4.66" />
        <rect class="cls-1" x="49.87" y="4.66" width="4.83" height="4.54" />
        <rect class="cls-1" x="5.96" width="5.65" height="6.24" />
        <rect class="cls-1" x="11.61" width="6.55" height="6.24" />
        <polygon
          class="cls-1"
          points="18.16 9.2 27.23 9.2 27.23 0 18.16 0 18.16 6.24 18.16 9.2"
        />
        <rect class="cls-1" x="45.39" width="4.49" height="4.66" />
        <rect class="cls-1" x="27.23" width="9.08" height="9.2" />
        <polygon
          class="cls-1"
          points="40.85 9.2 45.39 9.2 45.39 4.66 45.28 4.66 45.39 4.66 45.39 0 36.31 0 36.31 9.2 40.85 9.2"
        />
        <rect class="cls-1" width="5.96" height="6.24" />
      </g>
      <g id="left" class="left">
        <rect class="cls-1" y="12.35" width="5.96" height="5.92" />
        <rect class="cls-1" y="6.24" width="5.96" height="6.12" />
        <rect class="cls-1" y="30.64" width="6.81" height="5.8" />
        <rect class="cls-1" y="24.59" width="6.81" height="6.05" />
        <polygon
          class="cls-1"
          points="18.16 36.43 13.62 36.43 6.81 36.43 0 36.43 0 54.71 18.16 54.71 18.16 45.51 18.16 36.43"
        />
        <polygon
          class="cls-1"
          points="18.16 12.35 18.16 9.2 18.16 6.24 11.61 6.24 11.61 12.35 18.16 12.35"
        />
        <polygon
          class="cls-1"
          points="13.62 22.82 13.62 24.59 13.62 27.35 18.16 27.35 18.16 22.82 13.62 22.82"
        />
        <rect class="cls-1" x="5.96" y="6.24" width="5.65" height="6.12" />
        <polygon
          class="cls-1"
          points="18.16 12.35 11.61 12.35 11.61 18.28 13.62 18.28 13.62 18.22 13.62 18.28 18.16 18.28 18.16 12.35"
        />
        <polygon
          class="cls-1"
          points="13.62 30.64 13.62 31.89 18.16 31.89 18.16 27.35 13.62 27.35 13.62 30.64"
        />
        <rect class="cls-1" x="13.62" y="18.28" width="4.54" height="4.54" />
        <polygon
          class="cls-1"
          points="13.62 30.64 6.81 30.64 6.81 36.43 13.62 36.43 13.62 31.89 13.62 30.64"
        />
        <polygon
          class="cls-1"
          points="11.61 12.35 5.96 12.35 5.96 18.28 6.81 18.28 6.81 18.22 6.81 18.28 11.61 18.28 11.61 12.35"
        />
        <polygon
          class="cls-1"
          points="13.62 27.35 13.62 24.59 6.81 24.59 6.81 30.64 13.62 30.64 13.62 27.35"
        />
        <polygon
          class="cls-1"
          points="13.62 22.82 13.62 18.28 11.61 18.28 6.81 18.28 6.81 24.59 13.62 24.59 13.62 22.82"
        />
        <polygon
          class="cls-1"
          points="6.81 18.28 5.96 18.28 0 18.28 0 24.59 6.81 24.59 6.81 18.28"
        />
        <rect class="cls-1" x="13.62" y="31.89" width="4.54" height="4.54" />
      </g>
    </g>
  </svg>
`;

function initializeGame() {
  const game = document.getElementById("game");
  const bonusDialogue = document.getElementById("dialoguebonus");
    document.getElementById("resume");
    const bonusIcons = document.getElementById("bonuses"),
    bonusscore = document.getElementById("bonusscorewrap"),
    boomboom = document.getElementById("squarecrack");
    Array.from(game.querySelectorAll(".brick"));
    const castle = document.getElementById("castle");
    document.getElementById("console");
    const failDesc = document.getElementById("reason"),
    failDialogue = document.getElementById("dialoguefail"),
    highscorecounter = document.getElementById("highscore"),
    humanscore = document.getElementById("humanscore"),
    levelupContainer = document.getElementById("levelupcontainer"),
    levelupDesc = document.getElementById("levelupdesc"),
    levelupimg = document.getElementById("levelupimg"),
    overlay = document.getElementById("overlay"),
    progress = document.getElementById("progress"),
    progresscontainer = progress.closest(".reload-container"),
    restartbtn = document.getElementById("restart"),
    scanDialogue = document.getElementById("dialoguescan"),
    score = document.getElementById("badscore"),
    startbtn = document.getElementById("start"),
    statusContainer = document.getElementById("statuscontainer"),
    closebtn = document.getElementById("closegame");

  let brickGen,
    fallingBricks,
    totalscore = 0,
    humansfound = 0,
    bonusActivated = false,
    highscore = 0,
    reloaded = true,
    level = 0;

  const brickClass = "brick-wrap",
    humanClass = "human",
    badClass = "badbad";

  const l0limit = 4, // Scanner
    l1limit = 14, // bonus
    l2limit = 45, // Hover level
    l3limit = 120, // spotlight level
    radius = 28;

  function messages(totalscore, newhighscore) {
    // todo: Alert flag for bonusActivated, if bonusarray has all 4 categories
    //  if (bonusActivated ) {
    //   statusContainer.dataset.alert = "bonus";
    //  }
    if (totalscore >= 45) {
      statusContainer.dataset.alert = "bad";
    }
    if (humansfound >= 18) {
      statusContainer.dataset.alert = "human";
    }
    if (newhighscore) {
      highscore = totalscore;
      scoreboardupdate(highscorecounter, highscore.toLocaleString("en-US"));
      if (level !== 0 && totalscore >= 10) {
        // Don't show highscore in the first level
        console.log("highscoressssss");
        statusContainer.dataset.alert = "high-score";
      }
    }
  }

  function levelFind(currentLevel, score) {
    let newlevel;
    switch (currentLevel) {
      case 0:
        newlevel = score >= l0limit ? 1 : currentLevel;
        break;
      case 1:
        newlevel = score >= l2limit ? 2 : currentLevel;
        break;
      case 2:
        newlevel = score >= l3limit ? 3 : currentLevel;
        break;
    }
    // if currentLevel != newlevel
    return newlevel;
  }

  function levelSet(unlock) {
    let desc, img, title;
    function dismissdialogue(elem) {
      let active = true;
      elem.addEventListener("click", dismiss);
      setTimeout(() => {
        dismiss();
      }, 5000);
      function dismiss() {
        if (active) {
          elem.classList.remove("visible");
          resumeGame();
          active = false;
        }
      }
    }

    if (unlock == "scanner") {
      pauseGame();
      revealBoom();
      scanDialogue.classList.add("visible");
      game.classList = "l1";
      dismissdialogue(scanDialogue);
      level = 1;
    } else if (unlock == "bonus") {
      pauseGame();
      bonusDialogue.classList.add("visible");
      bonusActivated = true;
      bonusscore.classList.add("visible");
      dismissdialogue(bonusDialogue);
    } else {
      if (level == 2) {
        revealBoom(true); // Remove
        // hide scanner
        title = "Expert Mode!";
        desc = "Hovering on a square now reveals the entire thing!";
        img = hover;
      } else if (level == 3) {
        title = "Super Expert Mode!";
        desc = "Hovering squares now spotlights them.";
        img = spotlight;
      }
      // For every new level
      game.className = `l${level}`;
      failDialogue.classList = "bonusdialogue levelup visible";
      levelupDesc.innerHTML = desc;
      levelupDesc.previousElementSibling.innerHTML = title;
      levelupimg.src = celebrate;
      levelupContainer.firstElementChild.src = img;
    }
  }

  function scoreboardupdate(elem, num) {
    elem.classList = "animateout";
    elem.addEventListener("animationend", (event) => {
      elem.innerHTML = num.toLocaleString("en-US");
      elem.classList.add("animatein");
    });
  }

  function clearBricks() {
    document.querySelectorAll("." + brickClass).forEach((brick) => {
      brick.remove();
    }); // Delete the brix
  }

  function brickFall() {
    const activeBricks = game.querySelectorAll(
      "div." + brickClass + ":not(.clearing)"
    );
    const low = calcFall(Array.from(activeBricks));
    if (low.hit) {
      // Always if we're 50 away from the bottom
      if (!low.lowbrick.classList.contains("human")) {
        // only explode if we arent human
        explodeBrick(low.lowbrick, "bottom");
      } else {
        low.lowbrick.classList.add("clearing");
        humansfound = humansfound + 1;
        // take lowbrick out of comission
        humanscore.innerHTML = humansfound; // Right now this is a running total
        scoreboardupdate(humanscore, humansfound);
        countIt(low.lowbrick, "human", 1);
        console.log("human hit");
      }
    }
  }

  function calcFall(bricks) {
    let dist = 0,
      i = 0,
      lowbrick,
      hit = false,
      lowvalue = 0;

    const castleposleft = game.offsetWidth / 2 - castle.offsetWidth / 2;
    const castleposright = castleposleft + castle.offsetWidth;
    bricks.forEach((brick) => {
      i++;
      let bottom = game.offsetHeight - 50;
      let multiple = i / 10 < 3 ? i / 10 : 3; // Cap out at 3
      let rate = 1 + multiple; // Get faster as we produce more
      dist = parseInt(brick.style.top);
      brick.style.top = `${(dist += 5 * rate)}px`; // set the new top val

      // Logic for castle position
      let brickright = parseInt(brick.style.left);
      let brickleft = brickright + brick.offsetWidth;
      // if we're in the castle area, reset bottom value to less
      if (brickleft >= castleposleft && brickright <= castleposright) {
        bottom = bottom - castle.offsetHeight;
      }

      if (dist > lowvalue) {
        // Are we the lowest?
        lowvalue = dist;
        lowbrick = brick;
        hit = lowvalue + brick.offsetHeight >= bottom ? true : false; //are we the bottom?
      }
    });

    return {
      lowvalue,
      lowbrick,
      hit,
    };
  }

  function addBrick(bonusActivated, level) {
    bonusActivated = bonusActivated ? bonusActivated : false;
    let brickWrap = document.createElement("div");
    let brick = document.createElement("div");

    // Set the brick's initial position and speed
    brickWrap.classList.add(brickClass);
    brick.classList.add("brick");
    brickWrap.style.left = Math.random() * (game.offsetWidth - 70) + "px";
    brickWrap.style.top = "0px";
    brickWrap.style.transition = "top 500ms linear";

    // Choose a random type for the brick
    let type = Math.random();
    if (type < 0.233) {
      brickWrap.classList.add(humanClass);
    } else if (type < 0.33) {
      if (bonusActivated == true) {
        let bonus =
          type <= 0.24
            ? "bike"
            : type <= 0.27
            ? "stoplight"
            : type <= 0.3
            ? "crosswalk"
            : "hydrant";
        brickWrap.setAttribute("data-bonus", bonus);
        brickWrap.classList.add(bonus, "bonus");
      } else {
        brickWrap.classList.add(humanClass);
      }
    } else {
      brickWrap.classList.add(badClass);
    }
    // Add the brick to the game
    game.appendChild(brickWrap).appendChild(brick);
    // Add the the brick to the bricks
    // bricks.push(brickWrap);

    if (level == 3) {
      // todo: migrating all level settings to a single place
      brickMouseListen(brickWrap);
    }
  }

  let activebrick;

  function brickMouseListen(brick) {
    brick.addEventListener("mouseenter", (event) => {
      activebrick = brick;
    });
    brick.addEventListener("mouseleave", (event) => {
      // remove clip and active path
      brick.children[0].style["-webkit-clip-path"] = "inset(100%)";
      brick.children[0].style["clip-path"] = "inset(100%)";
      activebrick = undefined;
    });
  }

  function updatepos(event) {
    if (activebrick != undefined) {
      let x = event.clientX,
        y = event.clientY,
        elem = activebrick.children[0],
        pos = elem.getBoundingClientRect();

      x = x - pos.left;
      y = y - pos.top;
      let circle = `circle(${radius}px at ${x}px ${y}px)`;
      elem.style["-webkit-clip-path"] = circle;
      elem.style["clip-path"] = circle;
    }
  }

  function updateProgress() {
    let complete = 0;
    progresscontainer.classList.remove("ready");
    progress.value = complete;
    reloaded = false;

    let updator = setInterval(() => {
      // update progress
      complete = complete + 5;
      progress.value = complete;
    }, 100);

    setTimeout(() => {
      reloaded = true;
      progresscontainer.classList.add("ready");
      clearInterval(updator);
    }, 2000);
  }

  function getBricks() {
    let allbricks = Array.from(document.querySelectorAll(`.${brickClass}`));
    return allbricks;
  }

  function revealBoom(remove) {
    // listen for space keypress
    let scanner = function (event) {
      if (
        (event.key === "r" && reloaded) ||
        (event.key == "R" && reloaded) ||
        (event.key == " " && reloaded)
      ) {
        event.preventDefault();
        // Do this on mobile, also display it in CSS
        updateProgress();
        overlay.classList.add("scan");
        overlay.addEventListener("animationend", () => {
          overlay.classList.remove("scan");
        });

        let bricks = getBricks();
        bricks.forEach((brick) => {
          brick.classList.add("peekaboo");
          setTimeout(() => {
            brick.classList.remove("peekaboo");
          }, 1000);
        });
      } else {
        return;
      }
    };
    if (remove) {
      document.removeEventListener("keydown", scanner, false);
      progresscontainer.classList.remove("visible");
      console.log("REMOVE REMOVE REMOVE");
    } else {
      progresscontainer.classList.add("visible");
      document.addEventListener("keydown", scanner, false);
    }
  }

  function explodeBrick(target, reason) {
    target.appendChild(boomboom); // Put the svg into the brick
    target.classList.add("splode", "clicked");
    pauseGame(); // Stop the listen
    let icon = document.createElement("i");
    icon.classList.add("material-symbols-rounded", "warn");
    // icon.innerHTML = "priority_high"; // Add this back for afloating exclamation on click
    target.appendChild(icon);
    target.addEventListener("animationend", (e2) => {
      let time = 0;
      if (e2.animationName == "bottom1" && time == 0) {
        gameOver(reason); // Second animation, not the first
      }
    });
  }

  function handleClick(event) {
    let target = event.target;
    if (target.classList.contains(brickClass)) {
      if (target.classList.contains(humanClass)) {
        explodeBrick(target, humanClass);
      } else if (target.classList.contains("bonus")) {
        countIt(target, "bonus", 1, target.dataset.bonus);
      } else {
        countIt(target, "bad", 1);
      }
    }
  }

  function countIt(target, type, amount, icon) {
    target.classList.add("zap");
    let scorecontainer = document.createElement("h4");
    scorecontainer.classList.add("addscore");
    if (type == "bad") {
      totalscore = totalscore + amount;
      if (level == 0 && totalscore == 3 && bonusActivated != true) {
        // change to 10
        levelFind(level, totalscore);
        levelSet("scanner");
      } else if (
        level == 1 &&
        totalscore == l1limit &&
        bonusActivated != true
      ) {
        levelFind(level, totalscore);
        bonusActivated = true;
        levelSet("bonus");
      }
      scoreboardupdate(score, totalscore);
      scorecontainer.innerHTML = "+" + amount; // add floating +1
    } else if (type == "bonus") {
      if (bonusIcons.querySelector("." + icon) == null) {
        // todo: push icon to a bonuslist array if it's unique
        let bonusicon = document.createElement("span");
        bonusicon.classList.add("material-symbols-outlined", icon, "bonuses");
        bonusIcons.appendChild(bonusicon);
      }
    } else {
      //human
      scorecontainer.innerHTML = "+" + amount;
    }
    target.appendChild(scorecontainer);
    scorecontainer.addEventListener("animationend", () => {
      target.remove();
    });
  }
  //
  // Game lifecycle
  //
  function startGame(isfirst) {
    if (isfirst == true) {
      const introwrap = document.querySelectorAll(".intro")[0];
      introwrap.classList.add("out");
      introwrap.addEventListener("transitionend", (event) => {
        introwrap.remove();
      });
      addBrick(false, level);
    } else {
      addBrick(bonusActivated, level); // Show bonus bricks
    }
    if (level == 3) {
      document.addEventListener("mousemove", updatepos);
    } else {
      document.removeEventListener("mousemove", updatepos);
    }
    resumeGame();
  }

  function restartGame() {
    clearBricks();
    game.removeEventListener("click", handleClick);
    failDialogue.classList.remove("visible");
    score.innerHTML = 0;
    statusContainer.dataset.alert = ""; // remove alerts
    startGame(false); // add brick challenge if restarting
  }

  function pauseGame() {
    clearInterval(fallingBricks); // Stop the tracker
    clearInterval(brickGen); // Stop the drop
    game.removeEventListener("click", handleClick); // pause clicks
  }

  function resumeGame() {
    game.addEventListener("click", handleClick); // pause clicks
    brickGen = setInterval(() => {
      addBrick(bonusActivated, level);
    }, 900); // adjust to 900
    fallingBricks = setInterval(() => {
      brickFall();
    }, 100); //adjust to 100
  }

  function gameOver(reason) {
    let newhighscore = totalscore > highscore ? true : false;
    const desc =
      reason == humanClass
        ? "A human was mistaken as a bad."
        : "A bad slipped by and got to the castle.";
    const goodcount = document.getElementById("humancount"),
      badcount = document.getElementById("badcount");

    messages(totalscore, newhighscore);
    if (levelFind(level, totalscore) > level) {
      // New level
      level = levelFind(level, totalscore);
      levelSet();
    } else {
      // No new level
      failDialogue.classList = "bonusdialogue fail visible"; // hide the extra dialogue
      levelupimg.src = badFly;
    }
    const humantext =
      humansfound > 1
        ? ` still saved ${humansfound} humans.`
        : ` can try again forever.`;
    failDesc.innerHTML = desc;
    badcount.innerHTML = totalscore; // update bad num
    goodcount.innerHTML = humantext;
    // Regardless
    // levelupDialogue.classList.add("visible"); // show the dialogue
    clearInterval(fallingBricks); // Stop the tracker
    clearInterval(brickGen); // Stop the drop
    totalscore = 0;
    clearBricks();
  }
  function goodbye() {
    const baseurl = window.location.href.split("#")[0];
    window.location = baseurl;
  }

  // Init
  const start = () => startGame(true);
  const resume = () => {
    restartGame();
    restartbtn.blur();
  };
  startbtn.addEventListener("click", start);
  restartbtn.addEventListener("click", resume);
  closebtn.addEventListener("click", goodbye);

  return () => {
    startbtn.removeEventListener("click", start);
    restartbtn.removeEventListener("click", resume);
  };
}

var stoplight = "../static/item-stoplight-53247b633eed5a85.svg";

// Copyright 2023 Google LLC

const STEPS = ["home", "signup", "login", "store", "comment", "game"];

const DEFAULT_STEP = "home";

const ACTIONS = {
  comment: "send_comment",
  home: "home",
  login: "log_in",
  signup: "sign_up",
  store: "check_out",
  game: undefined,
};

const FORMS = {
  comment: "FORM_COMMENT",
  home: "FORM_HOME",
  login: "FORM_LOGIN",
  signup: "FORM_SIGNUP",
  store: "FORM_STORE",
  game: undefined,
};

const GUIDES = {
  comment: "GUIDE_COMMENT",
  home: "GUIDE_HOME",
  login: "GUIDE_LOGIN",
  signup: "GUIDE_SIGNUP",
  store: "GUIDE_STORE",
  game: undefined,
};

const LABELS = {
  comment: "Post comment",
  home: "View examples",
  login: "Log in",
  signup: "Sign up",
  store: "Buy now",
  game: undefined,
};

const RESULTS = {
  comment: "RESULT_COMMENT",
  home: "RESULT_HOME",
  login: "RESULT_LOGIN",
  signup: "RESULT_SIGNUP",
  store: "RESULT_STORE",
  game: undefined,
};

const getGame = (step) => {
  if (step === "game") {
    return gameHTML;
  }
  return A;
};

class RecaptchaDemo extends s {
  static get styles() {
    return demoCSS;
  }

  static properties = {
    /* Initial */
    animating: { type: Boolean, state: true, attribute: false },
    drawerOpen: { type: Boolean, state: true, attribute: false },
    sitemapOpen: { type: Boolean, state: true, attribute: false },
    step: { type: String },
    /* Result */
    score: { type: String },
    verdict: { type: String },
    reason: { type: String },
  };

  constructor() {
    super();
    /* Initial */
    this.animating = false;
    this.drawerOpen = true;
    this.sitemapOpen = false;
    this._step = DEFAULT_STEP;
    this.step = this._step;
    /* Result */
    this._score = undefined;
    this.score = this._score;
    this.verdict = undefined;
    this.reason = undefined;
    /* Other */
    this.cleanupGame = () => {};
    /* In the year of our lord 2023 */
    this._syncGameState = this.syncGameState.bind(this);
  }

  connectedCallback() {
    super.connectedCallback();
    this.syncGameState();
    window.addEventListener("hashchange", this._syncGameState);
    window.addEventListener("popstate", this._syncGameState);
  }

  disconnectedCallback() {
    this.syncGameState();
    window.removeEventListener("hashchange", this._syncGameState);
    window.removeEventListener("popstate", this._syncGameState);
    super.disconnectedCallback();
  }

  /* TODO: better/more reliable way to sync game state */
  syncGameState() {
    if (window.location.hash === "#game") {
      this.goToGame();
      return;
    }
    if (this.step === "game") {
      const stepFromRoute =
        STEPS.find((step) => {
          return window.location.pathname.includes(step);
        }) || DEFAULT_STEP;
      this.step = stepFromRoute;
      this.cleanupGame();
      this.renderGame();
    }
  }

  /* TODO: better/more reliable way to change button state */
  set score(value) {
    let oldValue = this._score;
    this._score = value;
    this.requestUpdate("score", oldValue);
    const buttonElement = document.querySelector("recaptcha-demo > button");
    if (buttonElement && this._score) {
      // TODO: redesign per b/278563766
      let updateButton = () => {};
      if (this.step === "comment") {
        updateButton = () => {
          buttonElement.innerText = "Play the game!";
        };
      } else {
        updateButton = () => {
          buttonElement.innerText = "Go to next demo";
        };
      }
      window.setTimeout(updateButton, 100);
    }
  }

  get score() {
    return this._score;
  }

  /* TODO: better/more reliable way to change button state */
  set step(value) {
    let oldValue = this._step;
    this._step = value;
    this.requestUpdate("step", oldValue);
    const buttonElement = document.querySelector("recaptcha-demo > button");
    if (buttonElement && !this.score) {
      buttonElement.innerText = LABELS[this._step];
    }
  }

  get step() {
    return this._step;
  }

  toggleDrawer() {
    this.animating = true;
    this.drawerOpen = !this.drawerOpen;
  }

  toggleSiteMap() {
    this.animating = true;
    this.sitemapOpen = !this.sitemapOpen;
  }

  goToGame() {
    this.animating = true;
    this.drawerOpen = false;
    this.sitemapOpen = false;
    this.step = "game";
    this.renderGame();
    window.setTimeout(() => {
      this.cleanupGame();
      this.cleanupGame = initializeGame();
    }, 1);
  }

  goToResult() {
    this.animating = true;
    const resultElement = this.shadowRoot.getElementById("result");
    const topOffset =
      Number(resultElement.getBoundingClientRect().top) +
      Number(resultElement.ownerDocument.defaultView.pageYOffset);
    window.setTimeout(() => {
      window.location.hash = "#result";
      window.scrollTo(0, topOffset);
    }, 100);
  }

  goToNextStep() {
    const nextIndex = STEPS.indexOf(this.step) + 1;
    const nextStep = STEPS[nextIndex] || DEFAULT_STEP;
    if (nextStep === "game") {
      this.goToGame();
      return;
    }
    this.animating = true;
    window.location.assign(`${window.location.origin}/${nextStep}`);
    // Don't need to assign this.step because of full page redirect
    return;
  }

  handleAnimation() {
    const currentlyRunning = this.shadowRoot.getAnimations({ subtree: true });
    this.animating = Boolean(currentlyRunning?.length || 0);
  }

  handleSlotchange() {
    // TODO: remove if not needed
  }

  handleSubmit() {
    if (this.score && this.verdict) {
      this.goToNextStep();
      return;
    }
    this.goToResult();
    // TODO: interrogate slotted button for callback?
  }

  renderGame() {
    B(getGame(this.step), document.body);
  }

  get BAR() {
    return x`
      <nav aria-label="Main Menu" id="bar">
        <h1 class="h1">BadFinder</h1>
        <h2 class="h2">
          A reCAPTCHA <abbr title="Demonstration">demo</abbr> site
        </h2>
        <mwc-icon-button
          @click=${this.toggleSiteMap}
          aria-controls="sitemap"
          aria-expanded="${this.sitemapOpen ? "true" : "false"}"
          aria-label="${this.sitemapOpen ? "Show site map" : "Hide site map"}"
          class="sitemapIcon"
          icon="${this.sitemapOpen ? "close" : "menu"}"
        ></mwc-icon-button>
      </nav>
    `;
  }

  get BUTTON() {
    return x`
      <div class="fields">
        <slot
          @click=${this.handleSubmit}
          @slotchange=${this.handleSlotchange}
        ></slot>
      </div>
    `;
  }

  get CONTENT() {
    return x`
      <main id="content">
        <div class="sticky">
          <div class="relative">
            <!-- bar -->
            ${this.BAR}
            <!-- forms -->
            ${this[FORMS[this.step]]}
            <!-- sitemap -->
            ${this.SITEMAP}
          </div>
        </div>
      </main>
    `;
  }

  get DRAWER() {
    return x`
      <aside id="drawer">
        <mwc-icon-button
          @click=${this.toggleDrawer}
          ?disabled=${this.step === "game"}
          aria-controls="drawer"
          aria-expanded="${this.drawerOpen ? "true" : "false"}"
          aria-label="${this.drawerOpen
            ? "Close the information panel"
            : "Open the information panel"}"
          class="drawerIcon"
          icon="${this.drawerOpen ? "close" : "code"}"
        ></mwc-icon-button>
        ${this[GUIDES[this.step]]}
        <p class="disclaimer">
          Response is shown here for convenience. We recommend using a backend
          to hide scores and reCAPTCHA responses for security reasons.
        </p>
      </aside>
    `;
  }

  get EXAMPLE() {
    return x`
      <!-- drawer -->
      ${this.DRAWER}
      <!-- content -->
      ${this.CONTENT}
    `;
  }

  get FORM_COMMENT() {
    return x`
      <form id="example">
        <fieldset>
          <legend><h3 class="h3">Comment form</h3></legend>
          <p>Click the "post comment" button to see if you can post or not.</p>
          <div class="fields">
            <label>
              <span>Comment</span>
              <textarea disabled>Great job protecting your users!</textarea>
            </label>
          </div>
        </fieldset>
        ${this.BUTTON}
      </form>
    `;
  }

  get FORM_HOME() {
    return x`
      <section id="example" class="home">
        <h3 class="h3">Stop the bad</h3>
        <p>
          BadFinder is a pretend world that's kinda like the real world. It's
          built to explore the different ways of using reCAPTCHA Enterprise to
          protect web sites and applications.
        </p>
        <p>
          Play the game, search the store, view the source, or just poke around
          and have fun!
        </p>
        <button @click=${this.handleSubmit} class="button" type="button">
          View examples
        </button>
      </section>
    `;
  }

  get FORM_LOGIN() {
    return x`
      <form id="example">
        <fieldset>
          <legend><h3 class="h3">Log in</h3></legend>
          <p>Click the "log in" button to see your score.</p>
          <div class="fields">
            <label>
              <span>Email</span>
              <input type="email" value="user@example.com" disabled />
            </label>
            <label>
              <span>Password</span>
              <input type="password" value="password" disabled />
            </label>
          </div>
        </fieldset>
        ${this.BUTTON}
      </form>
    `;
  }

  get FORM_SIGNUP() {
    return x`
      <form id="example">
        <fieldset>
          <legend><h3 class="h3">Secure Sign up</h3></legend>
          <p>
            Use with sign up forms to verify new accounts. Click the "sign up"
            button to see your score.
          </p>
          <div class="fields">
            <label>
              <span>Email</span>
              <input type="email" value="user@example.com" disabled />
            </label>
            <label>
              <span>Password</span>
              <input type="password" value="password" disabled />
            </label>
            <label>
              <span>Confirm Password</span>
              <input type="password" value="password" disabled />
            </label>
          </div>
        </fieldset>
        ${this.BUTTON}
      </form>
    `;
  }

  get FORM_STORE() {
    return x`
      <form id="example">
        <fieldset>
          <legend><h3 class="h3">Safe stores</h3></legend>
          <p>
            Add reCAPTCHA to stores and check out wizards to prevent fraud.
            Click the "buy now" button to see your score.
          </p>
          <div class="fields">
            <dl class="unstyled cart">
              <div class="item hydrant">
                <dt>
                  <img alt="Demo Product Hydrant" src="${hydrant$1}" />
                </dt>
                <dd>Hydrant</dd>
                <dd>
                  <label>
                    <span>Amount</span>
                    <input type="number" value="1" disabled />
                  </label>
                </dd>
              </div>
              <div class="item stoplight">
                <dt>
                  <img alt="Demo Product Stoplight" src="${stoplight}" />
                </dt>
                <dd>Stoplight</dd>
                <dd>
                  <label>
                    <span>Amount</span>
                    <input type="number" value="1" disabled />
                  </label>
                </dd>
              </div>
            </dl>
            <label>
              <span>Credit card</span>
              <input type="text" value="7777-8888-3333-2222" disabled />
            </label>
          </div>
        </fieldset>
        ${this.BUTTON}
      </form>
    `;
  }

  get GUIDE_CODE() {
    return `
    {
      "event": {
        "expectedAction": "${ACTIONS[this.step]}",
        ...
      },
      ...
      "riskAnalysis": {
        "reasons": [],
        "score": "${this.score || "?.?"}"
      },
      "tokenProperties": {
        "action": "${ACTIONS[this.step]}",
        ...
        "valid": ${this.reason !== 'Invalid token'}
      },
    }`
      .replace(/^([ ]+)[}](?!,)/m, "}")
      .replace(/([ ]{6})/g, "  ")
      .trim();
  }

  get GUIDE_COMMENT() {
    return x`
      <div id="guide">
        <div class="mask">
          <section class="text pattern">
            <h4 class="h1">Pattern</h4>
            <h5 class="h2">Prevent spam</h5>
            <p>
              Add reCAPTCHA to comment/ feedback forms and prevent bot-generated comments.
            </p>

            <a
              class="documentation"
              href="https://cloud.google.com/recaptcha-enterprise/docs/instrument-web-pages#user-action"
              target="_blank"
              ><span>Learn more</span><mwc-icon>launch</mwc-icon></a
            >
          </section>
          ${this[RESULTS[this.step]]}
        </div>
      </div>
    `;
  }

  get GUIDE_HOME() {
    return x`
      <div id="guide">
        <div class="mask">
          <section class="text pattern">
            <h4 class="h1">Pattern</h4>
            <h5 class="h2">Protect your entire site</h5>
            <p>
              Add to every page of your site when it loads. Tracking the
              behavior of legitimate users and bad ones between different pages
              and actions will improve scores.
            </p>
            <a
              class="documentation"
              href="https://cloud.google.com/recaptcha-enterprise/docs/instrument-web-pages#page-load"
              target="_blank"
              ><span>Learn more</span><mwc-icon>launch</mwc-icon></a
            >
          </section>
          ${this[RESULTS[this.step]]}
        </div>
      </div>
    `;
  }

  get GUIDE_LOGIN() {
    return x`
      <div id="guide">
        <div class="mask">
          <section class="text pattern">
            <h4 class="h1">Pattern</h4>
            <h5 class="h2">Prevent malicious log in</h5>
            <p>
              Add reCAPTCHA to user actions like logging in to prevent malicious
              activity on user accounts.
            </p>
            <a
              class="documentation"
              href="https://cloud.google.com/recaptcha-enterprise/docs/instrument-web-pages#user-action"
              target="_blank"
              ><span>Learn more</span><mwc-icon>launch</mwc-icon></a
            >
          </section>
          ${this[RESULTS[this.step]]}
        </div>
      </div>
    `;
  }

  get GUIDE_SCORE() {
    const score = this.score && this.score.slice(0, 3);
    const percentage = score && Number(score) * 100;
    let card = null;
    switch (this.verdict) {
      case "Not Bad":
        card = x`
          <p>reCAPTCHA is ${percentage || "???"}% confident you're not bad.</p>
          <img alt="Not Bad" src="${human}" />
        `;
        break;
        case "Bad":
          if (this.reason) {
            card = x`
              <p>Suspicious request. Reason: "${this.reason}".</p>
              <img alt="Bad" src="${badbad}" />
            `;
          } else {
            card = x`
              <p>reCAPTCHA is ${percentage || "???"}% confident you're not bad.</p>
              <img alt="Bad" src="${badbad}" />
            `;
          }
        break;
      default:
        card = x`
          <p>
            reCAPTCHA hasn't been run on this page yet. Click a button or
            initiate an action to run.
          </p>
          <img alt="Unknown" src="${badmorph}" />
        `;
    }
    return x`
      <div id="verdict">
        <div id="score">
          <div class="score">${score || "–"}</div>
          ${card}
        </div>
      </div>
    `;
  }

  get GUIDE_SIGNUP() {
    return x`
      <div id="guide">
        <div class="mask">
          <section class="text pattern">
            <h4 class="h1">Pattern</h4>
            <h5 class="h2">Run on sign up</h5>
            <p>
              Add reCAPTCHA to user interactions like signing up for new user
              accounts to prevent malicious actors from creating accounts.
            </p>
            <a
              class="documentation"
              href="https://cloud.google.com/recaptcha-enterprise/docs/instrument-web-pages#html-button"
              target="_blank"
              ><span>Learn more </span><mwc-icon>launch</mwc-icon></a
            >
          </section>
          ${this[RESULTS[this.step]]}
        </div>
      </div>
    `;
  }

  get GUIDE_STORE() {
    return x`
      <div id="guide">
        <div class="mask">
          <section class="text pattern">
            <h4 class="h1">Pattern</h4>
            <h5 class="h2">Prevent fraud</h5>
            <p>
              Add reCAPTCHA to user interactions like checkout, or add to cart
              buttons on payment pages or check out wizards to prevent fraud.
            </p>

            <a
              class="documentation"
              href="https://cloud.google.com/recaptcha-enterprise/docs/instrument-web-pages#user-action"
              target="_blank"
              ><span>Learn more</span><mwc-icon>launch</mwc-icon></a
            >
          </section>
          ${this[RESULTS[this.step]]}
        </div>
      </div>
    `;
  }

  get RESULT_COMMENT() {
    return x`
      <section id="result" class="text result">
        <h4 class="h1">Result</h4>
        ${this.GUIDE_SCORE}

        <section class="response">
          <h5 class="h1">Response Details</h5>

          <div class="code">
            <code>
              <pre>${this.GUIDE_CODE}</pre>
            </code>
          </div>
          <a
            class="log disabled"
            href="https://cloud.google.com/recaptcha-enterprise/docs/create-assessment"
            target="_blank"
            ><mwc-icon>description</mwc-icon><span>View Log</span></a
          >
        </section>
      </section>
    `;
  }

  get RESULT_HOME() {
    return x`
      <section id="result" class="text result">
        <h4 class="h1">Result</h4>
        ${this.GUIDE_SCORE}
        <section class="response">
          <h5 class="h1">Response Details</h5>

          <div class="code">
            <code>
              <pre>${this.GUIDE_CODE}</pre>
            </code>
          </div>
          <a
            class="log disabled"
            href="https://cloud.google.com/recaptcha-enterprise/docs/create-assessment"
            target="_blank"
            ><mwc-icon>description</mwc-icon><span>View Log</span></a
          >
          <p class="scoreExample">
            Use score responses to take or prevent end-user actions in the
            background. For example, filter scrapers from traffic statistics.
          </p>
        </section>
      </section>
    `;
  }

  get RESULT_LOGIN() {
    return x`
      <section id="result" class="text result">
        <h4 class="h1">Result</h4>
        ${this.GUIDE_SCORE}
        <section class="response">
          <h5 class="h1">Response Details</h5>
          <div class="code">
            <code>
              <pre>${this.GUIDE_CODE}</pre>
            </code>
          </div>
          <a
            class="log disabled"
            href="https://cloud.google.com/recaptcha-enterprise/docs/create-assessment"
            target="_blank"
            ><mwc-icon>description</mwc-icon><span>View log</span></a
          >
          <p class="scoreExample">
            Use score responses to take or prevent end-user actions in the
            background. For example, require a second factor to log in (MFA).
          </p>
        </section>
      </section>
    `;
  }

  get RESULT_SIGNUP() {
    return x`
      <section id="result" class="text result">
        <h4 class="h1">Result</h4>
        ${this.GUIDE_SCORE}
        <section class="response">
          <h5 class="h1">Response Details</h5>
          <div class="code">
            <code>
              <pre>${this.GUIDE_CODE}</pre>
            </code>
          </div>
          <a
            class="log disabled"
            href="https://cloud.google.com/recaptcha-enterprise/docs/create-assessment"
            target="_blank"
            ><mwc-icon>description</mwc-icon><span>View Log</span></a
          >
          <p class="scoreExample">
            Use score responses to take or prevent end-user actions in the
            background. For example, require email verification using MFA.
          </p>
        </section>
      </section>
    `;
  }

  get RESULT_STORE() {
    return x`
      <section id="result" class="text result">
        <h4 class="h1">Result</h4>
        ${this.GUIDE_SCORE}
        <section class="response">
          <h5 class="h1">Response Details</h5>
          <div class="code">
            <code>
              <pre>${this.GUIDE_CODE}</pre>
            </code>
          </div>
          <a
            class="log disabled"
            href="https://cloud.google.com/recaptcha-enterprise/docs/create-assessment"
            target="_blank"
            ><mwc-icon>description</mwc-icon><span>View Log</span></a
          >
          <p class="scoreExample">
            Use score responses to take or prevent end-user actions in the
            background. For example, queue risky transactions for manual review.
          </p>
        </section>
      </section>
    `;
  }

  get SITEMAP() {
    const tabindex = this.sitemapOpen ? "0" : "-1";
    return x`
      <nav id="sitemap">
        <div class="fade">
          <ul class="unstyled links">
            <li class="home">
              <a href="/" tabindex=${tabindex}>Home</a>
            </li>
            <li class="comments">
              <a href="/comment" tabindex=${tabindex}>Comments</a>
            </li>
            <li class="game">
              <a @click=${this.goToGame} href="#game" tabindex=${tabindex}
                >The game</a
              >
            </li>
            <li class="login">
              <a href="/login" tabindex=${tabindex}>Log in</a>
            </li>
            <li class="signup">
              <a href="/signup" tabindex=${tabindex}>Sign up</a>
            </li>
            <li class="store">
              <a href="/store" tabindex=${tabindex}>Store</a>
            </li>
          </ul>
          <section>
            <h3 class="h1">About</h3>
            <p>
              BadFinder is a pretend world that's kinda like the real world.
              It's built to explore the different ways of using reCAPTCHA
              Enterprise to protect web sites and applications.
            </p>
            <p>
              Play the game, search the store, view the source, or just poke
              around and have fun!
            </p>
          </section>
        </div>
      </nav>
    `;
  }

  render() {
    return x`
      <div
        @animationend=${this.handleAnimation}
        @animationstart=${this.handleAnimation}
        @transitionend=${this.handleAnimation}
        @transitionstart=${this.handleAnimation}
        class="${o({
          [this.step]: true,
          animating: this.animating,
          drawerOpen: this.step !== "game" && this.drawerOpen,
          drawerClosed: this.step === "game" || !this.drawerOpen,
          scored: this.score && this.verdict,
          sitemapOpen: this.sitemapOpen,
          sitemapClosed: !this.sitemapOpen,
          unscored: !this.score || !this.verdict,
        })}"
        id="demo"
      >
        ${this.EXAMPLE}
      </div>
    `;
  }
}

customElements.define("recaptcha-demo", RecaptchaDemo);
