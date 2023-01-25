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
// import { classMap } from "https://unpkg.com/lit@2.4.1/directives/class-map.js?module";
import "https://unpkg.com/@material/mwc-icon-button@0.27.0/mwc-icon-button.js?module";
import "https://unpkg.com/@material/mwc-icon@0.27.0/mwc-icon.js?module";

const STEPS = ["home", /* "game", */ "signup", "login", "store", "comment"];

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
      }
      label {
        display: block;
        font-weight: bold;
        letter-spacing: 0.5px;
        line-height: 1;
      }
      label:not(:last-child) {
        margin-bottom: var(--medium-space);
      }
      label > span {
        display: block;
        margin-bottom: var(--small-space);
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
        padding: var(--small-space);
        width: 100%;
      }
      a {
        color: hsl(var(--blue-60));
        display: block;
        font-weight: bold;
        text-decoration: none;
      }
      a:focus,
      a:hover,
      a:active {
        text-decoration: underline;
      }
      p,
      h1,
      h2,
      h3 {
        font: inherit;
        margin: 0;
        padding: 0;
      }
      /* Demo */
      :host {
        display: block;
      }
      :host,
      .demo {
        font-family: sans-serif;
        height: 100%;
        min-height: 100vh;
        max-width: 100%;
        width: 100%;
      }
      .demo {
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
        --drawer-glow: hsl(227, 63%, 14%, 18%);
        --drawer-highlight: 240, 52%, 11%;
        --drawer-lowlight: 240, 52%, 1%;
        --drawer-surface: 240, 52%, 6%;
        /*
        --drawer-lowlight: 245, 100%, 50%;
        --drawer-highlight: 0, 100%, 50%;
        */
        --content-glow: 235, 69%, 18%;
        --content-surface: 227, 63%, 9%;
        /* Sizes */
        --castle-bottom: 25vh;
        --drawer-width: 34vw;
        --example-width: 66vw;
        --land-bottom: 10vh;
        --large-space: 2rem;
        --medium-space: 1.5rem;
        --small-space: 0.75rem;
        --xlarge-space: 2.25rem;
        --xxlarge-space: 3rem;
        /* Timings */
        --drawer-lapse: 100ms;
        --full-lapse: 300ms;
        --half-lapse: 150ms;
      }
      .demo {
        color: white;
        display: grid;
        grid-template-columns: var(--drawer-width) var(--example-width);
        grid-template-rows: 1fr;
        transition: grid-template-columns var(--drawer-lapse) ease-out;
      }
      .demo.drawer-closed {
        grid-template-columns: 0vw 100vw;
      }
      .drawer {
        background: linear-gradient(
              to left,
              hsl(var(--drawer-ditch)) 1px,
              transparent 1px
            )
            0 0 / var(--drawer-width) 100vh no-repeat fixed,
          radial-gradient(
              ellipse,
              hsl(var(--drawer-lowlight), 75%) -10%,
              transparent 69%
            )
            calc((100vw - (var(--drawer-width) / 2)) * -1) -50vh / 100vw 200vh no-repeat
            fixed,
          radial-gradient(
              ellipse,
              hsl(var(--drawer-highlight), 75%) -10%,
              transparent 69%
            )
            calc(var(--drawer-width) / 2) -50vh / 100vw 200vh no-repeat fixed,
          linear-gradient(
              to right,
              hsl(var(--drawer-lowlight), 25%) 0,
              transparent 50%
            )
            0 0 / var(--drawer-width) 100vh no-repeat fixed,
          linear-gradient(
              to bottom,
              hsl(var(--drawer-lowlight), 35%) 0,
              transparent 50%
            )
            0 0 / var(--drawer-width) 100vh no-repeat fixed,
          linear-gradient(
              to left,
              hsl(var(--drawer-highlight), 15%) 0,
              transparent 25%
            )
            0 0 / var(--drawer-width) 100vh no-repeat fixed,
          linear-gradient(
              to top,
              hsl(var(--drawer-highlight), 15%) 0,
              transparent 50%
            )
            0 0 / var(--drawer-width) 100vh no-repeat fixed,
          linear-gradient(
              to right,
              hsl(var(--drawer-lowlight), 85%) 2px,
              transparent 2px
            )
            0 0 / var(--drawer-width) 100vh no-repeat fixed,
          linear-gradient(
              to bottom,
              hsl(var(--drawer-lowlight), 85%) 2px,
              transparent 2px
            )
            0 0 / var(--drawer-width) 100vh no-repeat fixed,
          linear-gradient(
              to left,
              hsl(var(--drawer-highlight), 85%) 1px,
              transparent 1px
            )
            0 0 / var(--drawer-width) 100vh no-repeat fixed,
          linear-gradient(
              to top,
              hsl(var(--drawer-highlight), 85%) 1px,
              transparent 1px
            )
            0 0 / var(--drawer-width) 100vh no-repeat fixed,
          hsl(var(--drawer-surface));
        box-shadow: 5px 0 9px 0 var(--drawer-glow);
        position: relative;
        z-index: 25;
      }
      .drawer > .drawer-close-icon {
        inset: -2px 0 auto auto;
        position: absolute;
        transition: opacity var(--half-lapse) ease-out;
        z-index: 4;
      }
      .drawer-closed .drawer > .drawer-close-icon {
        opacity: 0;
        transition-delay: 0;
      }
      .drawer-open .drawer > .drawer-close-icon {
        opacity: 1;
        transition-delay: var(--half-lapse);
      }
      /* Content */
      .content {
        /* This transform is required due to paint issues with animated elements in drawer
           However, using this also prevents background-attachment: fixed from functioning
           Therefore, background has to be moved to internal wrapper .sticky */
        /* transform: translateZ(0); */
      }
      .content {
        font-family: monospace;
      }
      .content .sticky-example {
        /* Due to CSS grid and sticky restrictions, have to add internal wrapper
           to get sticky behavior, centering in viewport behavior, and fixed background */
        display: grid;
        grid-template-columns: 1fr;
        grid-template-rows: auto 1fr;
        justify-content: safe center;
        min-height: 100vh;
        position: sticky;
        top: 0;
      }
      .drawer-open .content .sticky-example {
        --offset: calc(50% + (var(--drawer-width) / 2));
        background-position:
          /* castle */ var(--offset)
            var(--content-bottom),
          /* land */ var(--offset) var(--land-content-bottom),
          /* pink */ var(--offset) 75vh, /* purple */ var(--offset) 50vh,
          /* blue */ var(--offset) 18vh;
      }
      .content .sticky-example {
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
              hsl(var(--pink-40), 69%) 0,
              transparent 69%
            )
            center 75vh / 100vw 100vh no-repeat fixed,
          /* purple */
            radial-gradient(
              ellipse at bottom,
              hsl(var(--purple-30), 69%) 0,
              transparent 69%
            )
            center 50vh / 200vw 100vh no-repeat fixed,
          /* blue */
            radial-gradient(
              circle,
              hsl(var(--content-glow), 85%) 0,
              transparent 44%
            )
            center 18vh / 100vw 100vh no-repeat fixed,
          /* color */ hsl(var(--content-surface));
        transition: background-position var(--drawer-lapse) ease-out;
      }
      .content .h1,
      .content .h2 {
        font-family: "Press Start 2P", monospace;
        line-height: 1.25em;
      }
      /* Sitemap */
      .sitemap {
        align-items: center;
        background: linear-gradient(
            345deg,
            hsl(0, 0%, 0%, 25%) 5%,
            hsl(var(--content-surface)) 60%
          ),
          hsl(var(--content-surface));
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        font-family: monospace;
        justify-content: center;
        inset: 4.5rem 0 0 0;
        padding: var(--large-space);
        position: fixed;
        transition: transform var(--full-lapse) ease-out,
          opacity var(--drawer-lapse) var(--half-lapse) ease-in,
          padding-left var(--drawer-lapse) ease-out;
        z-index: 10;
      }
      .drawer-open .sitemap {
        padding-left: calc(var(--drawer-width) + var(--large-space));
      }
      .sitemap-open {
        opacity: 1;
        transform: translateY(0);
        transition-delay: 0, 0;
      }
      .sitemap-closed {
        opacity: 0;
        transform: translateY(100%);
        transition-delay: 0, var(--half-lapse);
      }
      .sitemap .links,
      .sitemap .h1,
      .sitemap p {
        max-width: 36rem;
        width: 100%;
      }
      .sitemap .links {
        display: grid;
        font-family: "Press Start 2P", monospace;
        gap: 2em;
        grid-template-columns: 1fr 1fr 1fr;
        grid-template-rows: 1fr;
        margin-bottom: 4rem;
      }
      .sitemap .h1,
      .sitemap p {
        margin-bottom: 1rem;
      }
      .sitemap .h1 {
        font-weight: bold;
      }
      /* Bar */
      .bar {
        align-items: center;
        background: hsl(var(--content-surface));
        display: flex;
        gap: var(--medium-space);
        justify-content: space-between;
        margin: 0 1rem var(--large-space) 0;
        padding: 0.5rem 1rem 0.5rem 0;
        position: sticky;
        top: 0;
        z-index: 20;
      }
      .bar mwc-icon-button {
        border: 0;
      }
      .bar .drawer-icon {
        background: hsl(var(--drawer-surface));
        border: 0 solid hsl(var(--drawer-ditch));
        border-width: 1px 1px 1px 0;
        border-radius: 0 6px 6px 0;
        box-shadow: 0 0 6px 1px var(--drawer-glow);
        padding: 6px;
        transition: transform var(--half-lapse) ease-in,
          opacity var(--half-lapse) linear;
        transform-origin: left top;
      }
      .logo {
        align-items: center;
        display: flex;
        gap: var(--small-space);
      }
      .bar .drawer-icon.show {
        opacity: 1;
        transform: scale(1) translateX(0);
      }
      .bar .drawer-icon.hide {
        opacity: 0;
        transform: scale(0.75) translateX(-100%);
      }
      .bar .h2 {
        color: hsl(var(--gray-40));
        font-size: 0.85rem;
      }
      /* Example */
      .example {
        box-sizing: border-box;
        margin: auto;
        max-width: 350px;
        width: 100%;
        padding-bottom: var(--xxlarge-space);
      }
      .example fieldset {
        margin-bottom: var(--xxlarge-space);
        position: relative;
        z-index: 2;
      }
      .example legend {
        text-align: center;
        width: 100%;
      }
      .example p {
        margin-bottom: var(--xxlarge-space);
      }
      .example legend .h2 {
        background: linear-gradient(
              90deg,
              transparent 0%,
              hsl(var(--purple-50), 25%) 20%,
              hsl(var(--purple-50), 25%) 80%,
              transparent 100%
            )
            center bottom / 100% 1px no-repeat scroll,
          radial-gradient(hsl(var(--purple-50), 25%), transparent 73%) center
            0.8em / 100% 100% no-repeat scroll,
          transparent;
        margin: 0 -2em 1rem;
        padding: 0 2em 1em;
        text-shadow: 2px 2px 0 black;
      }
      .example fieldset p {
        margin-bottom: var(--xlarge-space);
      }
      .example .h2 {
        font-size: 80%;
        line-height: 1.25em;
        margin-bottom: var(--medium-space);
        text-transform: uppercase;
      }
      .example.home .h2 {
        font-size: 130%;
        text-transform: none;
      }
      .example p {
        line-height: 1.65em;
      }
      /* Form */
      /* ... */
      /* Guide */
      .guide {
        overflow: hidden;
        transform: translateZ(0);
        width: 100%;
      }
      .guide-mask {
        width: var(--drawer-width);
      }
      .guide .h1 {
        border: 0 solid hsl(var(--drawer-ditch));
        border-width: 1px 0;
        letter-spacing: 0.5px;
        padding: var(--small-space) var(--large-space);
        text-transform: uppercase;
      }
      .guide .text:first-child .h1 {
        border-top-color: transparent;
      }
      .guide .h1,
      .guide .h2 {
        font-weight: bold;
      }
      .guide .h1 {
        line-height: 1.2;
      }
      .guide .h2 {
        line-height: 1.25em;
        margin-bottom: var(--small-space);
        text-transform: capitalize;
      }
      .guide .h2,
      .guide p,
      .guide a {
        padding: 0 var(--large-space);
      }
      .guide .h1,
      .guide p,
      .guide a,
      .guide code {
        margin-bottom: var(--large-space);
      }
      .guide p {
        line-height: 1.35em;
        max-width: 36em;
      }
      .guide code {
        /* TODO: background color */
        background: hsl(0, 0%, 100%, 4%);
        display: block;
        margin: 0 var(--large-space) var(--large-space);
        min-height: 4rem;
        padding: 1rem;
      }
      a {
        /* TODO: link color */
        --link-color: 218;
        align-items: center;
        color: hsl(var(--link-color), 27%, 68%);
        display: inline-flex;
      }
      a:focus,
      a:hover,
      a:active {
        color: hsl(var(--link-color), 35%, 68%);
        text-decoration: none;
      }
      a span {
        transition: var(--full-lapse) ease-out;
      }
      .links a:focus,
      .links a:hover,
      .links a:active,
      a:focus span,
      a:hover span,
      a:active span {
        text-decoration: white dashed underline 1px;
        text-underline-offset: 2px;
      }
      a mwc-icon {
        --mdc-icon-size: 1em;
        color: white;
        flex: 0 0 auto;
        text-decoration: none !important;
        transition: var(--full-lapse) ease-out;
      }
      a:focus mwc-icon,
      a:hover mwc-icon,
      a:active mwc-icon {
        transform: scale(1.25);
      }
      a span + mwc-icon,
      a mwc-icon + span {
        margin-left: 0.5em;
      }
      /* Store Card */
      dl.cart {
        margin-bottom: var(--xxlarge-space);
      }
      .cart .item {
        display: flex;
        align-items: top;
        justify-content: space-between;
        margin-bottom: var(--medium-space);
      }
      .cart img {
        height: auto;
        width: 50px;
      }
      .cart .stoplight img {
        margin-top: -13px; /* TODO: sigh magic numbers */
      }
      .cart dt {
        flex: 0 0 5em;
        margin-right: var(--medium-space);
        padding-top: 13px;
      }
      .cart dd:not(:last-child) {
        flex: 1 0 auto;
        margin-top: calc(1em + 13px + var(--small-space));
      }
      .cart dd:last-child {
        flex: 0 0 5em;
      }
      /* Guide Score */
      .score {
        align-items: center;
        display: flex;
        gap: 2rem;
        margin: 0 var(--large-space) var(--large-space);
      }
      .score dl {
        /* TODO: score blue */
        --custom-blue: 221, 91%, 65%;
        align-items: flex-start;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        line-height: 1;
      }
      .score dt {
        height: 1px;
        left: -10000px;
        overflow: hidden;
        position: absolute;
        top: auto;
        width: 1px;
      }
      .score dd {
        font-size: 1.25rem;
        line-height: 1.25em;
        text-transform: uppercase;
      }
      dd.score-result {
        color: hsl(var(--custom-blue));
        font-size: 2.5rem;
        font-weight: bold;
        line-height: 1em;
        text-indent: -0.1em;
      }
      dd.verdict-result {
        font-family: "Press Start 2P", monospace;
      }
      .score img {
        width: auto;
        height: 5rem;
      }
      /* Slotted Checkbox */
      ::slotted(div.g-recaptcha) {
        display: flex;
        justify-content: center;
        margin: 0 auto var(--xlarge-space);
        position: relative;
        z-index: 1;
      }
      /* Slotted Button / Button */
      .button {
        margin-bottom: var(--xxlarge-space);
      }
      ::slotted(button),
      .button {
        appearance: none;
        background: transparent /* hsl(var(--blue-50)) */;
        border: 0;
        border-radius: 0;
        color: inherit;
        cursor: pointer;
        display: inline-block;
        font: inherit;
        font-family: "Press Start 2P", monospace;
        font-size: 0.8rem;
        margin: 0 auto var(--medium-space);
        outline: 0;
        padding: 1rem 32px;
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
        /* TODO: timing variables */
        transition: border 50ms ease-out 0s,
          border-radius var(--half-lapse) ease-out 50ms,
          background 100ms ease 0s, box-shadow 200ms ease-out 0s,
          outline 50ms ease-out 0s, text-shadow 50ms ease-out 0s,
          transform 100ms ease-out 0s;
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
      ::slotted(button:focus),
      .button:focus,
      ::slotted(button:hover),
      .button:hover,
      ::slotted(button:active),
      .button:active {
        transform: scale(1.12);
      }
      ::slotted(button:focus)::after,
      .button:focus::after,
      ::slotted(button:focus)::before,
      .button:focus::before,
      ::slotted(button:hover)::after,
      .button:hover::after,
      ::slotted(button:hover)::before,
      .button:hover::before,
      ::slotted(button:active)::after,
      .button:active::after,
      ::slotted(button:active)::before,
      .button:active::before {
        transform: scale(0.89);
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
        border-radius: 22px;
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
        box-shadow: 1px 2px 42px 2px hsl(var(--blue-50), 45%);
      }
      ::slotted(button:active)::after,
      .button:active::after {
        /* Active Square Glow */
        box-shadow: 1px 2px 42px 2px rgba(0, 0, 0, 20%);
      }
      ::slotted(button:focus)::before,
      .button:focus::before,
      ::slotted(button:hover)::before,
      .button:hover::before {
        /* Focus/Hover Round Glow */
        box-shadow: 2px 2px 100px 20px hsl(var(--blue-50), 45%);
      }
      ::slotted(button:active)::before,
      .button:active::before {
        /* Active Round Glow */
        box-shadow: 2px 2px 100px 20px rgba(0, 0, 0, 20%);
      }
    `;
  }

  static properties = {
    drawerOpen: { type: Boolean, state: true, attribute: false },
    score: { type: String },
    siteMapOpen: { type: Boolean, state: true, attribute: false },
    step: { type: String },
    verdict: { type: String },
  };

  constructor() {
    super();
    this.step = "home";
    this.score = undefined;
    this.verdict = undefined;
    this.drawerOpen = true;
    this.siteMapOpen = false;
  }

  // willUpdate() {}

  // updated() {}

  toggleDrawer() {
    this.drawerOpen = !this.drawerOpen;
  }

  toggleSiteMap() {
    this.siteMapOpen = !this.siteMapOpen;
  }

  goToNextStep() {
    const nextIndex = STEPS.indexOf(this.step) + 1;
    const nextStep = STEPS[nextIndex];
    if (nextStep) {
      // this.step = nextStep;
      window.location.assign(`${window.location.origin}\\${nextStep}`);
    }
  }

  handleSlotchange() {
    // TODO: remove if not needed
  }

  handleSubmit() {
    if (this.score && this.verdict) {
      this.goToNextStep();
      return;
    }
    // TODO: interrogate slotted button for callback?
  }

  render() {
    const BUTTON = html`
      <slot
        @click=${this.handleSubmit}
        @slotchange=${this.handleSlotchange}
      ></slot>
    `;

    const FORMS = {
      home: html`
        <section class="example home">
          <h2 class="h2">Stop the bad</h2>
          <p>
            BadFinder is a pretend world that's kinda like the real world. It's
            built to let developers explore ways of using reCAPTCHA to protect
            your site. It can be deployed via a demosite here.
          </p>
          <p>
            Play the game, search the store, pretend to a be a BadBad, or just
            poke around and have fun!
          </p>
          <button @click=${this.handleSubmit} class="button" type="button">
            Continue
          </button>
        </section>
      `,
      store: html`
        <form class="example">
          <fieldset>
            <legend><h2 class="h2">Store example</h2></legend>
            <p>
              Some text prompting to solve the reCAPTCHA and/or click the button
              to see the verdict.
            </p>
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
          </fieldset>
          ${BUTTON}
        </form>
      `,
      login: html`
        <form class="example">
          <fieldset>
            <legend><h2 class="h2">Login example</h2></legend>
            <p>
              Some text prompting to solve the reCAPTCHA and/or click the button
              to see the verdict.
            </p>
            <label>
              <span>Email</span>
              <input type="email" value="user@example.com" disabled />
            </label>
            <label>
              <span>Password</span>
              <input type="password" value="password" disabled />
            </label>
          </fieldset>
          ${BUTTON}
        </form>
      `,
      comment: html`
        <form class="example">
          <fieldset>
            <legend><h2 class="h2">Comment example</h2></legend>
            <p>Some text prompting to solve the reCAPTCHA and/or click the button to see the verdict.</p>
            <label>
              <span>Comment</span>
              <textarea disabled />Good job.</textarea>
            </label>
          </fieldset>
          ${BUTTON}
        </form>
      `,
      signup: html`
        <form class="example">
          <fieldset>
            <legend><h2 class="h2">Signup example</h2></legend>
            <p>
              Some text prompting to solve the reCAPTCHA and/or click the button
              to see the verdict.
            </p>
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
          </fieldset>
          ${BUTTON}
        </form>
      `,
    };

    // TODO undefined case when it expires
    const SCORE = html`
      <div>
        <div class="score">
          <img src="../static/images/human-color-unoptimized.svg" alt="Human" />
          <dl class="unstyled">
            <dt>Score</dt>
            <dd class="score-result">
              ${(this.score && this.score.slice(0, 3)) || "???"}
            </dd>
            <dt>Verdict</dt>
            <dd class="verdict-result">Human</dd>
          </dl>
        </div>
        <p>
          How would you interpret the score? For example, what does a score of
          0.4 mean vs 0.6? How would you handle the final score? For example,
          would you output an error, fail silently, use a "redemption path", or
          supplement with another product?
        </p>
        <p>
          The 100+ signals ran on this page when it loaded and has a
          ${(this.score && Number(this.score.slice(0, 3))) * 100 || "???"}%
          confidence that you're a human.
        </p>
      </div>
    `;

    const CODE = `
    {
      "success": true, 
      "action": none 
      "challenge_ts": timestamp, 
      "hostname": string, 
      "error-codes": [...]
}`
      .replace(/([ ]+)/g, " ")
      .trim();

    const GUIDES = {
      home: html`
        <div class="guide">
          <div class="guide-mask">
            <section class="text static">
              <h1 class="h1">Pattern</h1>
              <h2 class="h2">On page load</h2>
              <p>
                A common pattern for homepages,reCAPTCHA runs on page load - the
                more pages that contain reCAPTCHA the better the signal, so even
                if you aren't making decisions based on what reCAPTCHA returns
                here, it can still enhance signals later on.
              </p>
              <p>
                What is this an example of (score when the page loads)? Why
                would you verify when the page loads? What kind of key? Why? How
                would you create? How would you load JS API? How would you set
                up the challenge?
              </p>
              <a
                href="https://cloud.google.com/recaptcha-enterprise/docs/instrument-web-pages#page-load"
                target="_blank"
              >
                <span>Learn more about scoring when the page loads</span>
                <mwc-icon>launch</mwc-icon>
              </a>
            </section>
            <section class="text">
              <h1 class="h1">Result</h1>
              ${SCORE}
              <h2 class="h1">Response Details</h2>
              <p>
                How would you fetch the token? For example, do you send a
                client-side request to a backend? How would you create an
                assessment? For example, do you require a backend to send a
                request to Google?
              </p>
              <code>
                <pre>${CODE}</pre>
              </code>
              <a href="#" target="_blank">
                <mwc-icon>description</mwc-icon>
                <span>View log</span>
              </a>
            </section>
          </div>
        </div>
      `,
      store: html`
        <div class="guide">
          <div class="guide-mask">
            <section class="text static">
              <h1 class="h1">Pattern</h1>
              <h2 class="h2">When users interact</h2>
              <p>
                What is this an example of (score on programmatic user action)?
                Why would you use an score programmatically on user interaction?
                What kind of key? Why? How would you create? How would you load
                JS API? How would you set up the challenge?
              </p>
              <a
                href="https://cloud.google.com/recaptcha-enterprise/docs/instrument-web-pages#user-action"
                target="_blank"
                ><span>Learn more about scoring when users interact</span>
                <mwc-icon>launch</mwc-icon></a
              >
            </section>
            <section class="text">
              <h1 class="h1">Result</h1>
              ${SCORE}
              <h2 class="h1">Response Details</h2>
              <p>
                How would you fetch the token? For example, do you send a
                client-side request to a backend? How would you create an
                assessment? For example, do you require a backend to send a
                request to Google?
              </p>
              <code>
                <pre>${CODE}</pre>
              </code>
              <a href="#" target="_blank">
                <mwc-icon>description</mwc-icon>
                <span>View log</span>
              </a>
            </section>
          </div>
        </div>
      `,
      login: html`
        <div class="guide">
          <div class="guide-mask">
            <section class="text static">
              <h1 class="h1">Pattern</h1>
              <h2 class="h2">On an HTML button</h2>
              <p>
                What is this an example of (score auto bind html button)? Why
                would you use an score auto bound to an html button? What kind
                of key? Why? How would you create? How would you load JS API?
                How would you set up the challenge?
              </p>
              <a
                href="https://cloud.google.com/recaptcha-enterprise/docs/instrument-web-pages#html-button"
                target="_blank"
                ><span
                  >Learn more about adding reCATPCHA on an HTML button</span
                >
                <mwc-icon>launch</mwc-icon></a
              >
            </section>
            <section class="text">
              <h1 class="h1">Result</h1>
              ${SCORE}
              <h2 class="h1">Response Details</h2>
              <p>
                How would you fetch the token? For example, do you send a
                client-side request to a backend? How would you create an
                assessment? For example, do you require a backend to send a
                request to Google?
              </p>
              <code>
                <pre>${CODE}</pre>
              </code>
              <a href="#" target="_blank">
                <mwc-icon>description</mwc-icon>
                <span>View log</span>
              </a>
            </section>
          </div>
        </div>
      `,
      comment: html`
        <div class="guide">
          <div class="guide-mask">
            <section class="text static">
              <h1 class="h1">Pattern</h1>
              <h2 class="h2">Automatically render a checkbox</h2>
              <p>
                What is this an example of (checkbox automatically rendered)?
                Why would you use a checkbox and automatically render it? What
                kind of key? Why? How would you create? How would you load JS
                API? How would you set up the challenge?
              </p>
              <a
                href="https://cloud.google.com/recaptcha-enterprise/docs/instrument-web-pages-with-checkbox#expandable-1"
                target="_blank"
                ><span
                  >Learn more about automatically rendering checkboxes</span
                >
                <mwc-icon>launch</mwc-icon></a
              >
            </section>
            <section class="text">
              <h1 class="h1">Result</h1>
              ${SCORE}
              <h2 class="h1">Response Details</h2>
              <p>
                How would you fetch the token? For example, do you send a
                client-side request to a backend? How would you create an
                assessment? For example, do you require a backend to send a
                request to Google?
              </p>
              <code>
                <pre>${CODE}</pre>
              </code>
              <a href="#" target="_blank">
                <mwc-icon>description</mwc-icon>
                <span>View log</span>
              </a>
            </section>
          </div>
        </div>
      `,
      signup: html`
        <div class="guide">
          <div class="guide-mask">
            <section class="text static">
              <h1 class="h1">Pattern</h1>
              <h2 class="h2">Explicitly render a checkbox</h2>
              <p>
                What is this an example of (checkbox explicitly rendered)? Why
                would you use a checkbox and explicitly render it? What kind of
                key? Why? How would you create? How would you load JS API? How
                would you set up the challenge?
              </p>
              <a
                href="https://cloud.google.com/recaptcha-enterprise/docs/instrument-web-pages-with-checkbox#expandable-2"
                target="_blank"
                ><span>Learn more about explicitly rendering checkboxes</span>
                <mwc-icon>launch</mwc-icon></a
              >
            </section>
            <section class="text">
              <h1 class="h1">Result</h1>
              ${SCORE}
              <h2 class="h1">Response Details</h2>
              <p>
                How would you fetch the token? For example, do you send a
                client-side request to a backend? How would you create an
                assessment? For example, do you require a backend to send a
                request to Google?
              </p>
              <code>
                <pre>${CODE}</pre>
              </code>
              <a href="#" target="_blank">
                <mwc-icon>description</mwc-icon>
                <span>View log</span>
              </a>
            </section>
          </div>
        </div>
      `,
    };

    const BAR = html`
      <div class="bar" id="bar">
        <mwc-icon-button
          icon="menu_open"
          aria-controls="drawer"
          aria-expanded="${this.drawerOpen ? "true" : "false"}"
          aria-label="Open the information panel"
          @click=${this.toggleDrawer}
          class="drawer-icon ${this.drawerOpen ? "hide" : "show"}"
        ></mwc-icon-button>
        <div class="logo">
          <mwc-icon>location_searching</mwc-icon>
          <h1 class="h1">BadFinder</h1>
          <h2 class="h2">reCAPTCHA Examples</h2>
        </div>
        <mwc-icon-button
          icon="${this.siteMapOpen ? "close" : "menu"}"
          aria-controls="sitemap"
          aria-expanded="${this.siteMapOpen ? "true" : "false"}"
          aria-label="${this.siteMapOpen ? "Show site map" : "Hide site map"}"
          @click=${this.toggleSiteMap}
          class="menu-icon ${this.siteMapOpen ? "show" : "hide"}"
        ></mwc-icon-button>
      </div>
    `;

    const SITEMAP = html`
      <nav
        id="sitemap"
        class="sitemap ${this.siteMapOpen ? "sitemap-open" : "sitemap-closed"}"
      >
        <ul class="unstyled links">
          <li><a href="/">Home</a></li>
          <li><a href="/game">Game</a></li>
          <li><a href="/login">Log in</a></li>
          <li><a href="/signup">Sign up</a></li>
          <li><a href="/store">Store</a></li>
          <li><a href="/comment">Comment</a></li>
        </ul>
        <h2 class="h1">About</h2>
        <p>
          BadFinder is a pretend world, built to give developers examples of
          using reCAPTCHA to protect your site. It can be deployed via a
          demosite here.
        </p>
        <p>
          You can play the game, search the store, pretend to a be a BadBad, or
          just poke around and have fun!
        </p>
      </nav>
    `;

    return html`
      <div
        id="demo"
        class="demo ${this.drawerOpen ? "drawer-open" : "drawer-closed"}"
      >
        <div id="drawer" class="drawer">
          <mwc-icon-button
            icon="close"
            aria-controls="drawer"
            aria-expanded="${this.drawerOpen ? "true" : "false"}"
            @click=${this.toggleDrawer}
            class="drawer-close-icon ${this.drawerOpen ? "show" : "hide"}"
          ></mwc-icon-button>
          ${GUIDES[this.step]}
        </div>
        <div id="content" class="content">
          <div class="sticky-example">${BAR} ${FORMS[this.step]}</div>
        </div>
        ${SITEMAP}
      </div>
    `;
  }
}

customElements.define("recaptcha-demo", RecaptchaDemo);
