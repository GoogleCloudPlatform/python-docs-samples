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

// TODO: productionize dependencies; network cascade is too slow
import {
  LitElement,
  css,
  html,
} from "https://unpkg.com/lit@2.4.1/index.js?module";
// import {
//   ref,
//   createRef,
// } from "https://unpkg.com/lit@2.4.1/directives/ref.js?module";
// import { asyncReplace } from "https://unpkg.com/lit@2.4.1/directives/async-replace.js?module";
import { classMap } from "https://unpkg.com/lit@2.4.1/directives/class-map.js?module";
import "https://unpkg.com/@material/mwc-icon-button@0.27.0/mwc-icon-button.js?module";
import "https://unpkg.com/@material/mwc-icon@0.27.0/mwc-icon.js?module";

const STEPS = ["home", "signup", "login", "store", "comment", "game"];

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
  comment: "Send comment",
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

class RecaptchaDemo extends LitElement {
  static get styles() {
    return css`
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
        --drawer-ditch: 227, 63%, 14%;
        --drawer-glow: hsl(227, 63%, 14%, 15%);
        --drawer-highlight: 240, 52%, 11%;
        --drawer-lowlight: 240, 52%, 1%;
        --drawer-surface: 240, 52%, 6%;
        --content-glow: 235, 69%, 18%;
        --content-surface: 227, 63%, 9%;
        --highlight-text: white;
        --lowlight-text: 218, 27%, 68%;
        --link-normal: 221, 92%, 71%;
        --link-focus: 221, 92%, 100%;
        /* Sizes */
        --bar-height: 4.6rem;
        --button-corners: 22px;
        --castle-bottom: 24vh;
        --drawer-width: 30vw;
        --example-width: 70vw;
        --land-bottom: 10vh;
        --line-length: 36em;
        --line-short: 1.38em;
        --line-tall: 1.68em;
        --size-gigantic: 5.2rem;
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
      }
      /* Links */
      a {
        color: hsl(var(--link-normal));
        text-decoration: none;
        vertical-align: bottom;
      }
      #guide a {
        font-weight: normal;
      }
      a span {
        display: inline;
        white-space: break-space;
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
        font-family: sans-serif;
        font-size: var(--size-normal);
        height: 100%;
        min-height: 100vh;
        max-width: 100%;
        width: 100%;
      }
      #demo {
        color: var(--highlight-text);
        display: grid;
        grid-template-columns: var(--drawer-width) var(--example-width);
        grid-template-rows: 1fr;
        transition: grid-template-columns var(--drawer-lapse) ease-out 0s;
      }
      #demo.drawerClosed {
        grid-template-columns: 0vw 100vw;
      }
      #drawer {
        background: linear-gradient(
              to left,
              hsl(var(--drawer-ditch)) 1px,
              transparent 1px
            )
            0 0 / var(--drawer-width) 100vh no-repeat fixed,
          radial-gradient(
              ellipse,
              hsl(var(--drawer-lowlight), 70%) -10%,
              transparent 69%
            )
            calc((100vw - (var(--drawer-width) / 2)) * -1) -50vh / 100vw 200vh no-repeat
            fixed,
          radial-gradient(
              ellipse,
              hsl(var(--drawer-highlight), 70%) -10%,
              transparent 69%
            )
            calc(var(--drawer-width) / 2) -50vh / 100vw 200vh no-repeat fixed,
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
        box-shadow: 5px 0 9px 0 var(--drawer-glow);
        position: relative;
        z-index: 25;
      }
      #drawer > .drawerCloseIcon {
        inset: auto 0 auto auto;
        position: absolute;
        transition: opacity var(--half-lapse) ease-out 0s;
        z-index: 4;
      }
      .drawerClosed #drawer > .drawerCloseIcon {
        opacity: 0;
        transition-delay: 0;
      }
      .drawerOpen #drawer > .drawerCloseIcon {
        opacity: 1;
        transition-delay: var(--half-lapse);
      }
      /* Content */
      #content {
        /* This transform is required due to paint issues with animated elements in drawer
           However, using this also prevents background-attachment: fixed from functioning
           Therefore, background has to be moved to internal wrapper .sticky */
        font-family: monospace;
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
          /* castle */ var(--offset)
            var(--content-bottom),
          /* land */ var(--offset) var(--land-content-bottom),
          /* pink */ var(--offset) 75vh, /* purple */ var(--offset) 50vh,
          /* blue */ var(--offset) var(--bar-height);
      }
      #content .sticky {
        --content-bottom: calc(100vh - var(--castle-bottom));
        --land-content-bottom: calc(100vh - var(--land-bottom));
        background: 
          /* castle */ url("../static/images/castle-alternate-unoptimized.svg")
            center var(--content-bottom) / auto var(--castle-bottom) no-repeat
            fixed,
          /* land */ url("../static/images/land-unoptimized.svg") center
            var(--land-content-bottom) / auto var(--land-bottom) no-repeat fixed,
          /* pink */
            radial-gradient(
              ellipse at bottom,
              hsl(var(--pink-40), 64%) 0,
              transparent 69%
            )
            center 75vh / 100vw 100vh no-repeat fixed,
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
              hsl(var(--content-glow), 80%) 0,
              transparent 44%
            )
            center var(--bar-height) / 100vw 100vh no-repeat fixed,
          /* color */ hsl(var(--content-surface));
        transition: background-position var(--drawer-lapse) ease-out 0s;
      }
      /* Sitemap */
      #sitemap {
        align-items: center;
        background: linear-gradient(
            345deg,
            hsl(0, 0%, 0%, 15%) 5%,
            hsl(var(--content-surface)) 58%
          ),
          hsl(var(--content-surface));
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        font-family: monospace;
        justify-content: center;
        inset: var(--bar-height) 0 0 0;
        margin-left: 0;
        padding: var(--size-huge);
        position: absolute;
        transition: transform var(--full-lapse) ease-out 0s,
          padding-left var(--drawer-lapse) ease-out 0s,
          margin-left var(--drawer-lapse) ease-out 0s;
        z-index: 10;
      }
      #sitemap .fade {
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
      }
      .sitemapClosed #sitemap .fade {
        opacity: 0;
      }
      .drawerOpen #sitemap {
        --stack-size: calc(var(--drawer-width) + var(--size-huge));
        margin-left: calc(var(--stack-size) * -1);
        padding-left: var(--stack-size);
      }
      #demo:not(.animating).sitemapClosed #sitemap {
        max-height: 0;
        max-width: 0;
        opacity: 0;
        z-index: -4;
      }
      #sitemap .links,
      #sitemap .h1,
      #sitemap p {
        max-width: var(--line-length);
        width: 100%;
      }
      #sitemap .links {
        display: grid;
        font-family: "Press Start 2P", monospace;
        gap: var(--size-huge);
        grid-template-areas: "row-1-1 row-1-2 row-1-3" "row-2-1 row-2-2 row-2-3" ". row-3-2 .";
        grid-template-columns: auto auto auto;
        grid-template-rows: auto auto;
        margin-bottom: var(--size-gigantic);
      }
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
        grid-area: row-1-1;
      }
      #sitemap .home {
        grid-area: row-1-2;
      }
      #sitemap .comments {
        grid-area: row-2-2;
      }
      #sitemap .login {
        grid-area: row-3-2;
      }
      #sitemap .signup {
        grid-area: row-1-3;
      }
      #sitemap .store {
        grid-area: row-2-3;
      }
      /* Bar */
      #bar {
        align-items: center;
        background: hsl(var(--content-surface));
        display: flex;
        gap: var(--size-xlarge);
        justify-content: space-between;
        margin: 0 var(--size-normal) var(--size-huge) 0;
        padding: var(--size-mini) var(--size-normal) var(--size-mini) 0;
        position: sticky;
        top: 0;
        z-index: 20;
      }
      #bar mwc-icon-button {
        border: 0;
      }
      #bar .drawerIcon {
        background: hsl(var(--drawer-surface));
        border: 0 solid hsl(var(--drawer-ditch));
        border-width: 1px 1px 1px 0;
        border-radius: 0 6px 6px 0;
        box-shadow: 0 0 6px 1px var(--drawer-glow);
        padding: 6px;
        transition: transform var(--quick-lapse) ease-in 0s,
          opacity var(--quick-lapse) linear 0s;
        transform-origin: left top;
      }
      .drawerClosed #bar .drawerIcon {
        opacity: 1;
        transform: scale(1) translateX(0);
      }
      .drawerOpen #bar .drawerIcon {
        opacity: 0;
        transform: scale(0.75) translateX(-100%);
      }
      #bar .drawerIcon[disabled],
      .drawerClosed #bar .drawerIcon[disabled],
      .drawerOpen #bar .drawerIcon[disabled] {
        --mdc-theme-text-disabled-on-light: hsl(var(--gray-40));
        opacity: 0.74;
      }
      .logo {
        align-items: center;
        display: flex;
        font-family: "Press Start 2P", monospace;
        gap: var(--size-small);
      }
      .logoWord {
        align-items: flex-end;
        display: flex;
        gap: var(--size-large);
      }
      .logo .h1 {
        font-size: var(--size-large);
      }
      .logo .h2 {
        color: hsl(var(--gray-40));
        font-size: var(--size-normal);
      }
      .logo .h2 abbr {
        text-decoration: none;
      }
      /* Example */
      #example {
        box-sizing: border-box;
        margin: auto;
        max-width: max(400px, var(--line-length));
        padding-bottom: var(--size-jumbo);
      }
      #example fieldset {
        margin-bottom: var(--size-jumbo);
        position: relative;
        z-index: 2;
      }
      #example .fields {
        margin: 0 auto;
        max-width: 400px;
      }
      #example legend {
      }
      #example .h3 {
        background: linear-gradient(
              90deg,
              transparent 0%,
              hsl(var(--content-glow)) 20%,
              hsl(var(--content-glow)) 80%,
              transparent 100%
            )
            center bottom / 100% 1px no-repeat scroll,
          radial-gradient(hsl(var(--content-glow), 50%), transparent 73%) center
            0.8em / 100% 100% no-repeat scroll,
          transparent;
        color: var(--highlight-text);
        font-family: "Press Start 2P", monospace;
        font-size: var(--size-xlarge);
        letter-spacing: 2px;
        line-height: var(--size-large-em);
        margin: 0 -3em var(--size-normal) -3em;
        padding: 0 3em var(--size-normal);
        text-transform: capitalize;
      }
      #example.home .h3 {
        font-size: var(--size-huge);
        text-transform: none;
      }
      #example .h3 {
        text-shadow: -2px -2px 0 hsl(var(--content-glow)),
          2px 2px 0 hsl(var(--content-surface));
      }
      #example p {
        text-shadow: -1px -1px 0 hsl(var(--content-glow)),
          1px 1px 0 hsl(var(--content-surface));
      }
      #example p {
        color: hsl(var(--lowlight-text));
        line-height: var(--line-tall);
        margin-bottom: var(--bar-height);
      }
      #example.home p {
        margin-bottom: var(--size-huge);
      }
      #example.home p:last-of-type {
        margin-bottom: var(--size-jumbo);
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
        font-family: sans-serif;
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
      }
      .mask {
        width: var(--drawer-width);
      }
      #guide .h1,
      #guide .h2 {
        color: var(--highlight-text);
        font-size: var(--size-large);
        font-weight: bold;
      }
      #guide .h1 {
        border: 0 solid hsl(var(--drawer-ditch));
        border-width: 1px 0;
        letter-spacing: 1px;
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
        text-transform: capitalize;
      }
      #guide p {
        color: hsl(var(--lowlight-text));
        line-height: var(--line-short);
        max-width: var(--line-length);
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
        position: relative;
      }
      #guide a.log {
        inset: auto var(--size-normal) var(--size-small) auto;
        position: absolute;
      }
      /* Guide Score */
      #score {
        align-items: flex-end;
        display: flex;
        gap: var(--size-huge);
        margin: 0 var(--size-xhuge) var(--line-short);
        padding-top: var(--size-micro);
      }
      #score dl {
        align-items: flex-start;
        display: flex;
        flex-direction: column;
        gap: var(--size-small);
        line-height: 1;
      }
      #score dt {
        height: 1px;
        left: -10000px;
        overflow: hidden;
        position: absolute;
        top: auto;
        width: 1px;
      }
      dd.score {
        color: hsl(var(--link-normal));
        font-family: sans-serif;
        font-size: var(--size-jumbo);
        font-weight: bold;
        line-height: 1;
        text-indent: -0.1em;
      }
      dd.verdict {
        color: var(--highlight-text);
        font-family: "Press Start 2P", monospace;
        font-size: var(--size-xlarge);
        line-height: 1;
        text-transform: uppercase;
      }
      #score img {
        height: calc(var(--size-jumbo) * 2);
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
      #score {
        animation: var(--full-lapse) ease-out 0s 2 alternate both running
          scoreBump;
        transform-origin: left center;
      }
      .unscored #score {
        animation-play-state: paused;
      }
      .scored #score {
        animation-play-state: running;
      }
      #guide .response,
      #verdict p,
      .scoreExample {
        transition: opacity var(--full-lapse) ease-out var(--half-lapse);
      }
      .unscored #guide .response,
      .unscored #verdict p,
      .unscored .scoreExample {
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
        font-family: "Press Start 2P", monospace;
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
        box-shadow: 1px 2px var(--size-jumbo) 2px hsl(var(--blue-50), 38%);
      }
      ::slotted(button:active)::after,
      .button:active::after {
        /* Active Square Glow */
        box-shadow: 1px 2px var(--size-jumbo) 2px hsl(0, 0%, 0%, 12%);
      }
      ::slotted(button:focus)::before,
      .button:focus::before,
      ::slotted(button:hover)::before,
      .button:hover::before {
        /* Focus/Hover Round Glow */
        box-shadow: 2px 2px var(--size-xgigantic) 20px hsl(var(--blue-50), 38%);
      }
      ::slotted(button:active)::before,
      .button:active::before {
        /* Active Round Glow */
        box-shadow: 2px 2px var(--size-xgigantic) 20px hsl(0, 0%, 0%, 12%);
      }
      /* Game */
      #game {
        align-items: center;
        display: flex;
        font-size: 4rem;
        inset: 0 0 0 0;
        justify-content: center;
        margin-top: -4rem;
        position: absolute;
      }
    `;
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
  };

  constructor() {
    super();
    /* Initial */
    this.animating = false;
    this.drawerOpen = true;
    this.sitemapOpen = false;
    this._step = "home";
    this.step = this._step;
    /* Result */
    this._score = undefined;
    this.score = this._score;
    this.verdict = undefined;
  }

  /* TODO: better/more reliable way to change button state */

  set score(value) {
    let oldValue = this._score;
    this._score = value;
    this.requestUpdate("score", oldValue);
    const buttonElement = document.getElementsByTagName("button")[0];
    if (buttonElement && this._score && this.step !== "comment") {
      window.setTimeout(() => {
        buttonElement.innerText = "Go to next demo";
      }, 100);
    }
  }

  get score() {
    return this._score;
  }

  set step(value) {
    let oldValue = this._step;
    this._step = value;
    this.requestUpdate("step", oldValue);
    const buttonElement = document.getElementsByTagName("button")[0];
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

  goToResult() {
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
    const nextStep = STEPS[nextIndex];
    if (nextStep) {
      this.animating = true;
      window.location.assign(`${window.location.origin}\\${nextStep}`);
    }
  }

  handleAnimation(event) {
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

  get BAR() {
    return html`
      <nav aria-label="Main Menu" id="bar">
        <mwc-icon-button
          @click=${this.toggleDrawer}
          aria-controls="drawer"
          aria-expanded="${this.drawerOpen ? "true" : "false"}"
          aria-label="Open the information panel"
          class="drawerIcon"
          ?disabled=${this.step === "game"}
          icon="menu_open"
        ></mwc-icon-button>
        <div class="logo">
          <mwc-icon>location_searching</mwc-icon>
          <div class="logoWord">
            <h1 class="h1">BadFinder</h1>
            <h2 class="h2">
              reCAPTCHA <abbr title="Demonstration">Demo</abbr>
            </h2>
          </div>
        </div>
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
    return html`
      <div class="fields">
        <slot
          @click=${this.handleSubmit}
          @slotchange=${this.handleSlotchange}
        ></slot>
      </div>
    `;
  }

  get CONTENT() {
    return html`
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
    return html`
      <aside id="drawer">
        <mwc-icon-button
          @click=${this.toggleDrawer}
          aria-controls="drawer"
          aria-expanded="${this.drawerOpen ? "true" : "false"}"
          class="drawerCloseIcon"
          icon="close"
        ></mwc-icon-button>
        ${this[GUIDES[this.step]]}
      </aside>
    `;
  }

  get EXAMPLE() {
    return html`
      <!-- drawer -->
      ${this.DRAWER}
      <!-- content -->
      ${this.CONTENT}
    `;
  }

  get FORM_COMMENT() {
    return html`
      <form id="example">
        <fieldset>
          <legend><h3 class="h3">Confident comments</h3></legend>
          <p>Add reCAPTCHA Enterprise to comment and contact forms to prevent spam. Click the "send comment" button to see the result.</p>
          <div class="fields">
          <label>
            <span>Comment</span>
            <textarea disabled />Good job protecting your users.</textarea>
          </label>
          </div>
        </fieldset>
        ${this.BUTTON}
      </form>
    `;
  }

  get FORM_HOME() {
    return html`
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
    return html`
      <form id="example">
        <fieldset>
          <legend><h3 class="h3">Locked log in</h3></legend>
          <p>
            Add reCAPTCHA Enterprise to log in forms to secure accounts. Click
            the "log in" button to see the result.
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
          </div>
        </fieldset>
        ${this.BUTTON}
      </form>
    `;
  }

  get FORM_SIGNUP() {
    return html`
      <form id="example">
        <fieldset>
          <legend><h3 class="h3">Secure Sign up</h3></legend>
          <p>
            Add reCAPTCHA Enterprise to sign up forms to verify new accounts.
            Click the "sign up" button to see the result.
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
    return html`
      <form id="example">
        <fieldset>
          <legend><h3 class="h3">Safe stores</h3></legend>
          <p>
            Add reCAPTCHA to stores and check out wizards to prevent fraud.
            Click the "buy now" button to see the result.
          </p>
          <div class="fields">
            <dl class="unstyled cart">
              <div class="item hydrant">
                <dt>
                  <img
                    alt="Demo Product Hydrant"
                    src="../static/images/item-hydrant-unoptimized.svg"
                  />
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
                  <img
                    alt="Demo Product Stoplight"
                    src="../static/images/item-stoplight-unoptimized.svg"
                  />
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

  // TODO: move game in
  get GAME() {
    return html`
      <aside id="drawer"></aside>
      <main id="content">
        <div class="sticky">
          <div class="relative">
            <!-- bar -->
            ${this.BAR}
            <!-- game -->
            <div id="game">Coming soon!</div>
            <!-- sitemap -->
            ${this.SITEMAP}
          </div>
        </div>
      </main>
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
        "invalidReason": null,
        "valid": true
      },
    }`
      .replace(/^([ ]+)[}](?!,)/m, "}")
      .replace(/([ ]{6})/g, "  ")
      .trim();
  }

  get GUIDE_COMMENT() {
    return html`
      <div id="guide">
        <div class="mask">
          <section class="text pattern">
            <h4 class="h1">Pattern</h4>
            <h5 class="h2">When users interact</h5>
            <p>
              Add reCAPTCHA Enterprise verification on important user
              interactions like posting user comments. Verification can be added
              to JavaScript events. With a score-based site key, you can include
              reCAPTCHA Enterprise throughout your site without requiring users
              to solve CAPTCHA challenges.
            </p>
            <a
              class="documentation"
              href="https://cloud.google.com/recaptcha-enterprise/docs/instrument-web-pages#user-action"
              target="_blank"
              ><span>Learn more about scoring when users interact</span
              ><mwc-icon>launch</mwc-icon></a
            >
          </section>
          ${this[RESULTS[this.step]]}
        </div>
      </div>
    `;
  }

  get GUIDE_HOME() {
    return html`
      <div id="guide">
        <div class="mask">
          <section class="text pattern">
            <h4 class="h1">Pattern</h4>
            <h5 class="h2">On page load</h5>
            <p>
              Try running reCAPTCHA Enterprise on every page load. With a
              score-based site key, you can include reCAPTCHA Enterprise
              throughout your site without requiring users to solve CAPTCHA
              challenges. We recommend that you include reCAPTCHA Enterprise on
              every page of your site because data about how real users and bots
              transition between different pages and actions improves scores.
            </p>
            <a
              class="documentation"
              href="https://cloud.google.com/recaptcha-enterprise/docs/instrument-web-pages#page-load"
              target="_blank"
              ><span>Learn more about scoring when the page loads</span
              ><mwc-icon>launch</mwc-icon></a
            >
          </section>
          ${this[RESULTS[this.step]]}
        </div>
      </div>
    `;
  }

  get GUIDE_LOGIN() {
    return html`
      <div id="guide">
        <div class="mask">
          <section class="text pattern">
            <h4 class="h1">Pattern</h4>
            <h5 class="h2">When users interact</h5>
            <p>
              Add reCAPTCHA Enterprise verification on important user
              interactions like logging into user accounts. Verification can be
              added to JavaScript events. With a score-based site key, you can
              include reCAPTCHA Enterprise throughout your site without
              requiring users to solve CAPTCHA challenges.
            </p>
            <a
              class="documentation"
              href="https://cloud.google.com/recaptcha-enterprise/docs/instrument-web-pages#user-action"
              target="_blank"
              ><span>Learn more about scoring when users interact</span
              ><mwc-icon>launch</mwc-icon></a
            >
          </section>
          ${this[RESULTS[this.step]]}
        </div>
      </div>
    `;
  }

  // TODO: undefined case when it expires
  get GUIDE_SCORE() {
    return html`
      <div id="verdict">
        <div id="score">
          <img alt="Human" src="../static/images/human-color-unoptimized.svg" />
          <dl class="unstyled">
            <dt>Score</dt>
            <dd class="score">
              ${(this.score && this.score.slice(0, 3)) || "?.?"}
            </dd>
            <dt>Verdict</dt>
            <dd class="verdict">${(this.verdict && "Human") || "?????"}</dd>
          </dl>
        </div>
        <p>
          The 100+ signals ran on this page when it loaded and has a
          ${(this.score && Number(this.score.slice(0, 3))) * 100 || "???"}%
          confidence that you're a human. Based on the score, you can take an
          appropriate action in the background instead of blocking traffic.
        </p>
      </div>
    `;
  }

  get GUIDE_SIGNUP() {
    return html`
      <div id="guide">
        <div class="mask">
          <section class="text pattern">
            <h4 class="h1">Pattern</h4>
            <h5 class="h2">On an HTML button</h5>
            <p>
              Add reCAPTCHA Enterprise verification on important user
              interactions like signing up for new user accounts. Verification
              can be added to simple HTML buttons. With a score-based site key,
              you can include reCAPTCHA Enterprise throughout your site without
              requiring users to solve CAPTCHA challenges.
            </p>
            <a
              class="documentation"
              href="https://cloud.google.com/recaptcha-enterprise/docs/instrument-web-pages#html-button"
              target="_blank"
              ><span>Learn more about adding reCAPTCHA on an HTML button</span
              ><mwc-icon>launch</mwc-icon></a
            >
          </section>
          ${this[RESULTS[this.step]]}
        </div>
      </div>
    `;
  }

  get GUIDE_STORE() {
    return html`
      <div id="guide">
        <div class="mask">
          <section class="text pattern">
            <h4 class="h1">Pattern</h4>
            <h5 class="h2">When users interact</h5>
            <p>
              Add reCAPTCHA Enterprise verification on important user
              interactions like making purchases. Verification can be added to
              JavaScript events. With a score-based site key, you can include
              reCAPTCHA Enterprise throughout your site without requiring users
              to solve CAPTCHA challenges.
            </p>
            <a
              class="documentation"
              href="https://cloud.google.com/recaptcha-enterprise/docs/instrument-web-pages#user-action"
              target="_blank"
              ><span>Learn more about scoring when users interact</span
              ><mwc-icon>launch</mwc-icon></a
            >
          </section>
          ${this[RESULTS[this.step]]}
        </div>
      </div>
    `;
  }

  get RESULT_COMMENT() {
    return html`
      <section id="result" class="text result">
        <h4 class="h1">Result</h4>
        ${this.GUIDE_SCORE}
        <p class="scoreExample">
          For example, send suspicious comments to moderation.
        </p>
        <section class="response">
          <h5 class="h1">Response Details</h5>
          <p>
            Use reCAPTCHA Enterprise to generate a token for the action. After
            the token is generated, send the reCAPTCHA token to your backend and
            create an assessment within two minutes.
          </p>
          <div class="code">
            <code>
              <pre>${this.GUIDE_CODE}</pre>
            </code>
            <a
              class="log"
              href="https://cloud.google.com/recaptcha-enterprise/docs/create-assessment"
              target="_blank"
              ><mwc-icon>description</mwc-icon
              ><span>Creating assessments</span></a
            >
          </div>
        </section>
      </section>
    `;
  }

  get RESULT_HOME() {
    return html`
      <section id="result" class="text result">
        <h4 class="h1">Result</h4>
        ${this.GUIDE_SCORE}
        <p class="scoreExample">
          For example, filter scrapers from traffic statistics.
        </p>
        <section class="response">
          <h5 class="h1">Response Details</h5>
          <p>
            Use reCAPTCHA Enterprise to generate a token for the action. After
            the token is generated, send the reCAPTCHA token to your backend and
            create an assessment within two minutes.
          </p>
          <div class="code">
            <code>
              <pre>${this.GUIDE_CODE}</pre>
            </code>
            <a
              class="log"
              href="https://cloud.google.com/recaptcha-enterprise/docs/create-assessment"
              target="_blank"
              ><mwc-icon>description</mwc-icon
              ><span>Creating assessments</span></a
            >
          </div>
        </section>
      </section>
    `;
  }

  get RESULT_LOGIN() {
    return html`
      <section id="result" class="text result">
        <h4 class="h1">Result</h4>
        ${this.GUIDE_SCORE}
        <p class="scoreExample">
          For example, require MFA (Multi Factor Authentication).
        </p>
        <section class="response">
          <h5 class="h1">Response Details</h5>
          <p>
            Use reCAPTCHA Enterprise to generate a token for the action. After
            the token is generated, send the reCAPTCHA token to your backend and
            create an assessment within two minutes.
          </p>
          <div class="code">
            <code>
              <pre>${this.GUIDE_CODE}</pre>
            </code>
            <a
              class="log"
              href="https://cloud.google.com/recaptcha-enterprise/docs/create-assessment"
              target="_blank"
              ><mwc-icon>description</mwc-icon
              ><span>Creating assessments</span></a
            >
          </div>
        </section>
      </section>
    `;
  }

  get RESULT_SIGNUP() {
    return html`
      <section id="result" class="text result">
        <h4 class="h1">Result</h4>
        ${this.GUIDE_SCORE}
        <p class="scoreExample">For example, require email verification.</p>
        <section class="response">
          <h5 class="h1">Response Details</h5>
          <p>
            Use reCAPTCHA Enterprise to generate a token for the action. After
            the token is generated, send the reCAPTCHA token to your backend and
            create an assessment within two minutes.
          </p>
          <div class="code">
            <code>
              <pre>${this.GUIDE_CODE}</pre>
            </code>
            <a
              class="log"
              href="https://cloud.google.com/recaptcha-enterprise/docs/create-assessment"
              target="_blank"
              ><mwc-icon>description</mwc-icon
              ><span>Creating assessments</span></a
            >
          </div>
        </section>
      </section>
    `;
  }

  get RESULT_STORE() {
    return html`
      <section id="result" class="text result">
        <h4 class="h1">Result</h4>
        ${this.GUIDE_SCORE}
        <p class="scoreExample">
          For example, queue risky transactions for manual review.
        </p>
        <section class="response">
          <h5 class="h1">Response Details</h5>
          <p>
            Use reCAPTCHA Enterprise to generate a token for the action. After
            the token is generated, send the reCAPTCHA token to your backend and
            create an assessment within two minutes.
          </p>
          <div class="code">
            <code>
              <pre>${this.GUIDE_CODE}</pre>
            </code>
            <a
              class="log"
              href="https://cloud.google.com/recaptcha-enterprise/docs/create-assessment"
              target="_blank"
              ><mwc-icon>description</mwc-icon
              ><span>Creating assessments</span></a
            >
          </div>
        </section>
      </section>
    `;
  }

  get SITEMAP() {
    return html`
      <nav id="sitemap">
        <div class="fade">
          <ul class="unstyled links">
            <li class="home"><a href="/">Home</a></li>
            <li class="comments"><a href="/comment">Comments</a></li>
            <li class="game"><a href="/game">The game</a></li>
            <li class="login"><a href="/login">Log in</a></li>
            <li class="signup"><a href="/signup">Sign up</a></li>
            <li class="store"><a href="/store">Store</a></li>
          </ul>
          <h3 class="h1">About</h3>
          <p>
            BadFinder is a pretend world that's kinda like the real world. It's
            built to explore the different ways of using reCAPTCHA Enterprise to
            protect web sites and applications.
          </p>
          <p>
            Play the game, search the store, view the source, or just poke
            around and have fun!
          </p>
        </div>
      </nav>
    `;
  }

  render() {
    let CONTENTS;
    if (this.step === "game") {
      CONTENTS = this.GAME;
    } else {
      CONTENTS = this.EXAMPLE;
    }

    return html`
      <div
        @animationend=${this.handleAnimation}
        @animationstart=${this.handleAnimation}
        @transitionend=${this.handleAnimation}
        @transitionstart=${this.handleAnimation}
        class="${classMap({
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
        ${CONTENTS}
      </div>
    `;
  }
}

customElements.define("recaptcha-demo", RecaptchaDemo);
