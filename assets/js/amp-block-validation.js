!function(e){var t={};function r(n){if(t[n])return t[n].exports;var a=t[n]={i:n,l:!1,exports:{}};return e[n].call(a.exports,a,a.exports,r),a.l=!0,a.exports}r.m=e,r.c=t,r.d=function(e,t,n){r.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},r.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},r.t=function(e,t){if(1&t&&(e=r(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(r.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var a in e)r.d(n,a,function(t){return e[t]}.bind(null,a));return n},r.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return r.d(t,"a",t),t},r.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},r.p="",r(r.s=45)}([function(e,t){!function(){e.exports=this.wp.element}()},function(e,t){!function(){e.exports=this.wp.i18n}()},function(e,t){!function(){e.exports=this.wp.components}()},function(e,t){!function(){e.exports=this.wp.data}()},function(e,t){!function(){e.exports=this.wp.blockEditor}()},function(e,t,r){e.exports=r(23)()},,,function(e,t,r){var n=r(25);e.exports=function(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{},a=Object.keys(r);"function"==typeof Object.getOwnPropertySymbols&&(a=a.concat(Object.getOwnPropertySymbols(r).filter(function(e){return Object.getOwnPropertyDescriptor(r,e).enumerable}))),a.forEach(function(t){n(e,t,r[t])})}return e}},,function(e,t){!function(){e.exports=this.lodash}()},function(e,t,r){"use strict";var n=r(8),a=r.n(n),o=r(0),i=(r(5),r(1)),c=r(2),l=r(4),u=r(3),s=["core/paragraph","core/heading","core/code","core/quote","core/subhead"],m=["core/image","core/video"];r.d(t,"a",function(){return d}),r.d(t,"d",function(){return f}),r.d(t,"b",function(){return O}),r.d(t,"c",function(){return g}),r.d(t,"e",function(){return C});var b=[{value:"nodisplay",label:Object(i.__)("No Display","amp"),notAvailable:["core-embed/vimeo","core-embed/dailymotion","core-embed/hulu","core-embed/reddit","core-embed/soundcloud"]},{value:"fixed",label:Object(i.__)("Fixed","amp"),notAvailable:["core-embed/soundcloud"]},{value:"responsive",label:Object(i.__)("Responsive","amp"),notAvailable:["core-embed/soundcloud"]},{value:"fixed-height",label:Object(i.__)("Fixed height","amp"),notAvailable:[]},{value:"fill",label:Object(i.__)("Fill","amp"),notAvailable:["core-embed/soundcloud"]},{value:"flex-item",label:Object(i.__)("Flex Item","amp"),notAvailable:["core-embed/soundcloud"]},{value:"intrinsic",label:Object(i.__)("Intrinsic","amp"),notAvailable:["core/video","core-embed/youtube","core-embed/facebook","core-embed/instagram","core-embed/vimeo","core-embed/dailymotion","core-embed/hulu","core-embed/reddit","core-embed/soundcloud"]}],d=function(e,t){return"core/shortcode"!==t&&"core/gallery"!==t||(e.attributes||(e.attributes={}),e.attributes.ampCarousel={type:"boolean"},e.attributes.ampLightbox={type:"boolean"}),"core/image"===t&&(e.attributes||(e.attributes={}),e.attributes.ampLightbox={type:"boolean"}),s.includes(t)&&(e.attributes||(e.attributes={}),e.attributes.ampFitText={default:!1},e.attributes.minFont={default:6,source:"attribute",selector:"amp-fit-text",attribute:"min-font-size"},e.attributes.maxFont={default:72,source:"attribute",selector:"amp-fit-text",attribute:"max-font-size"},e.attributes.height={default:"core/image"===t?200:10*Math.ceil(7.2),source:"attribute",selector:"amp-fit-text",attribute:"height"}),(0===t.indexOf("core-embed")||m.includes(t))&&(e.attributes||(e.attributes={}),e.attributes.ampLayout={type:"string"},e.attributes.ampNoLoading={type:"boolean"}),e},f=function(e,t,r){var n=r.text||"",a="",i={layout:"fixed-height"};if("core/shortcode"===t.name&&I(r)){if(r.ampLightbox||L(r.text||"")&&(n=P(r.text)),r.ampCarousel){if(T(n)&&(n=S(n)),!r.ampLightbox)return r.text!==n?Object(o.createElement)(o.RawHTML,null,n):e}else n=T(r.text||"")?r.text:r.text.replace("[gallery","[gallery amp-carousel=false");if(r.ampLightbox&&!L(n)&&(n=n.replace("[gallery","[gallery amp-lightbox=true")),r.text!==n)return Object(o.createElement)(o.RawHTML,null,n)}else if("core/paragraph"!==t.name||r.ampFitText){if(s.includes(t.name)&&r.ampFitText){if(r.minFont&&(i["min-font-size"]=r.minFont),r.maxFont&&(i["max-font-size"]=r.maxFont),r.height&&(i.height=r.height),"core/paragraph"===t.name){var c="<amp-fit-text";for(var l in i){c+=" "+l+'="'+i[l]+'"'}return c+=">"+p(r.content)+"</amp-fit-text>",Object(o.cloneElement)(e,{key:"new",value:c})}return i.children=e,Object(o.createElement)("amp-fit-text",i)}}else if((a=p(r.content))!==r.content)return Object(o.cloneElement)(e,{key:"new",value:a});return e},p=function(e){var t=/<amp-fit-text\b[^>]*>(.*?)<\/amp-fit-text>/.exec(e),r=e;return t&&t[1]&&(r=t[1]),r},h=function(e){for(var t=[{value:"",label:Object(i.__)("Default","amp")}],r=0,n=b;r<n.length;r++){var a=n[r];!a.notAvailable.includes(e)&&t.push({value:a.value,label:a.label})}return t},O=function(e,t,r){var n={};return"core/shortcode"===t.name?e:"amp/"===t.name.substr(0,4)?e:(r.ampLayout&&(n["data-amp-layout"]=r.ampLayout),r.ampNoLoading&&(n["data-amp-noloading"]=r.ampNoLoading),r.ampLightbox&&(n["data-amp-lightbox"]=r.ampLightbox),r.ampCarousel&&(n["data-amp-carousel"]=r.ampCarousel),a()({},n,e))},g=function(e){return function(t){var r,n=t.attributes,a=n.text,i=n.ampLayout,c=t.setAttributes,l=t.name;if("core/shortcode"===l){if(T(a||"")&&c({text:S(a)}),L(a||"")&&c({text:P(a)}),""===(r=x(t)))return Object(o.createElement)(e,t)}else"core/gallery"===l?r=w(t):"core/image"===l?r=A(t):m.includes(l)||0===l.indexOf("core-embed/")?r=v(t):s.includes(l)&&(r=y(t));return i&&"nodisplay"===i?[r]:Object(o.createElement)(o.Fragment,null,Object(o.createElement)(e,t),r)}},v=function(e){return e.isSelected?Object(o.createElement)(l.InspectorControls,null,Object(o.createElement)(c.PanelBody,{title:Object(i.__)("AMP Settings","amp")},Object(o.createElement)(j,e),Object(o.createElement)(_,e))):null},j=function(e){var t=e.name,r=e.attributes.ampLayout,n=e.setAttributes,a=Object(i.__)("AMP Layout","amp");return"core/image"===t&&(a=Object(i.__)("AMP Layout (modifies width/height)","amp")),Object(o.createElement)(c.SelectControl,{label:a,value:r,options:h(t),onChange:function(t){n({ampLayout:t}),"core/image"===e.name&&function(e,t){var r=e.attributes,n=e.setAttributes;switch(t){case"fixed-height":r.height||n({height:400}),r.ampLightbox&&n({ampLightbox:!1});break;case"fixed":r.height||n({height:400}),r.width||n({width:608})}}(e,t)}})},_=function(e){var t=e.attributes.ampNoLoading,r=e.setAttributes,n=Object(i.__)("AMP Noloading","amp");return Object(o.createElement)(c.ToggleControl,{label:n,checked:t,onChange:function(){return r({ampNoLoading:!t})}})},y=function(e){var t=e.isSelected,r=e.attributes,n=e.setAttributes,a=r.ampFitText,u=r.minFont,s=r.maxFont,m=r.height,b=[{name:"small",shortName:Object(i._x)("S","font size","amp"),size:14},{name:"regular",shortName:Object(i._x)("M","font size","amp"),size:16},{name:"large",shortName:Object(i._x)("L","font size","amp"),size:36},{name:"larger",shortName:Object(i._x)("XL","font size","amp"),size:48}];if(!t)return null;var d=Object(i.__)("Automatically fit text to container","amp");return a&&(s=parseInt(s,10),m=parseInt(m,10),u=parseInt(u,10)),Object(o.createElement)(l.InspectorControls,null,Object(o.createElement)(c.PanelBody,{title:Object(i.__)("AMP Settings","amp"),className:a?"is-amp-fit-text":""},Object(o.createElement)(c.ToggleControl,{label:d,checked:a,onChange:function(){return n({ampFitText:!a})}})),a&&Object(o.createElement)(o.Fragment,null,Object(o.createElement)(c.TextControl,{label:Object(i.__)("Height","amp"),value:m,min:1,onChange:function(e){n({height:e})}}),s>m&&Object(o.createElement)(c.Notice,{status:"error",isDismissible:!1},Object(i.__)("The height must be greater than the max font size.","amp")),Object(o.createElement)(c.PanelBody,{title:Object(i.__)("Minimum font size","amp")},Object(o.createElement)(c.FontSizePicker,{fallbackFontSize:14,value:u,fontSizes:b,onChange:function(e){e||(e=6),parseInt(e,10)<=s&&n({minFont:e})}})),u>s&&Object(o.createElement)(c.Notice,{status:"error",isDismissible:!1},Object(i.__)("The min font size must less than the max font size.","amp")),Object(o.createElement)(c.PanelBody,{title:Object(i.__)("Maximum font size","amp")},Object(o.createElement)(c.FontSizePicker,{fallbackFontSize:48,value:s,fontSizes:b,onChange:function(e){e||(e=72),n({maxFont:e,height:Math.max(e,m)})}}))))},x=function(e){var t=e.isSelected;if(!I(e.attributes)||!t)return null;var r=Object(u.select)("amp/block-editor").hasThemeSupport();return Object(o.createElement)(l.InspectorControls,null,Object(o.createElement)(c.PanelBody,{title:Object(i.__)("AMP Settings","amp")},r&&Object(o.createElement)(k,e),Object(o.createElement)(E,e)))},E=function(e){var t=e.attributes,r=t.ampLightbox,n=t.linkTo,a=t.ampLayout,l=e.setAttributes;return Object(o.createElement)(c.ToggleControl,{label:Object(i.__)("Add lightbox effect","amp"),checked:r,onChange:function(e){l({ampLightbox:!r}),e&&("fixed-height"===a&&l({ampLayout:"fixed"}),n&&"none"!==n&&l({linkTo:"none"}))}})},k=function(e){var t=e.attributes.ampCarousel,r=e.setAttributes;return Object(o.createElement)(c.ToggleControl,{label:Object(i.__)("Display as carousel","amp"),checked:t,onChange:function(){return r({ampCarousel:!t})}})},A=function(e){return e.isSelected?Object(o.createElement)(l.InspectorControls,null,Object(o.createElement)(c.PanelBody,{title:Object(i.__)("AMP Settings","amp")},Object(o.createElement)(j,e),Object(o.createElement)(_,e),Object(o.createElement)(E,e))):null},w=function(e){if(!e.isSelected)return null;var t=Object(u.select)("amp/block-editor").hasThemeSupport();return Object(o.createElement)(l.InspectorControls,null,Object(o.createElement)(c.PanelBody,{title:Object(i.__)("AMP Settings","amp")},t&&Object(o.createElement)(k,e),Object(o.createElement)(E,e)))},S=function(e){return e.replace(" amp-carousel=false","")},P=function(e){return e.replace(" amp-lightbox=true","")},T=function(e){return-1!==e.indexOf("amp-carousel=false")},L=function(e){return-1!==e.indexOf("amp-lightbox=true")},I=function(e){return e.text&&-1!==e.text.indexOf("gallery")},C=function(){var e=Object(u.select)("amp/block-editor"),t=e.getDefaultStatus,r=e.getPossibleStatuses,n=Object(u.select)("core/editor").getEditedPostAttribute;if("amp_story"===n("type"))return!0;var a=n("meta");return a&&a.amp_status&&r().includes(a.amp_status)?"enabled"===a.amp_status:"enabled"===t()}},function(e,t){!function(){e.exports=this.wp.hooks}()},,function(e,t){!function(){e.exports=this.wp.compose}()},,,,,,,,,function(e,t,r){"use strict";var n=r(24);function a(){}function o(){}o.resetWarningCache=a,e.exports=function(){function e(e,t,r,a,o,i){if(i!==n){var c=new Error("Calling PropTypes validators directly is not supported by the `prop-types` package. Use PropTypes.checkPropTypes() to call them. Read more at http://fb.me/use-check-prop-types");throw c.name="Invariant Violation",c}}function t(){return e}e.isRequired=e;var r={array:e,bool:e,func:e,number:e,object:e,string:e,symbol:e,any:e,arrayOf:t,element:e,elementType:e,instanceOf:t,node:e,objectOf:t,oneOf:t,oneOfType:t,shape:t,exact:t,checkPropTypes:o,resetWarningCache:a};return r.PropTypes=r,r}},function(e,t,r){"use strict";e.exports="SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED"},function(e,t){e.exports=function(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}},function(e,t,r){"use strict";var n={};r.r(n),r.d(n,"getBlockValidationErrors",function(){return c}),r.d(n,"hasThemeSupport",function(){return l}),r.d(n,"isNativeAMP",function(){return u}),r.d(n,"getDefaultStatus",function(){return s}),r.d(n,"getPossibleStatuses",function(){return m});var a=r(8),o=r.n(a),i=r(3);function c(e,t){return e.errorsByClientId[t]||[]}function l(e){return Boolean(e.hasThemeSupport)}function u(e){return Boolean(e.isNativeAMP)}function s(e){return e.defaultStatus}function m(e){return e.possibleStatuses}Object(i.registerStore)("amp/block-editor",{reducer:function(e){return e},selectors:n,initialState:o()({},window.ampBlockEditor)})},,,,,function(e,t,r){var n=r(42),a=r(43),o=r(44);e.exports=function(e){return n(e)||a(e)||o()}},,,,,,,,,,,function(e,t){e.exports=function(e){if(Array.isArray(e)){for(var t=0,r=new Array(e.length);t<e.length;t++)r[t]=e[t];return r}}},function(e,t){e.exports=function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}},function(e,t){e.exports=function(){throw new TypeError("Invalid attempt to spread non-iterable instance")}},function(e,t,r){"use strict";r.r(t);var n={};r.r(n),r.d(n,"addValidationError",function(){return x}),r.d(n,"resetValidationErrors",function(){return E}),r.d(n,"updateReviewLink",function(){return k});var a={};r.r(a),r.d(a,"getValidationErrors",function(){return A}),r.d(a,"getBlockValidationErrors",function(){return w}),r.d(a,"getReviewLink",function(){return S}),r.d(a,"isSanitizationAutoAccepted",function(){return P});var o=r(12),i=r(3),c=r(10),l=r(1),u=function(){var e=Object(i.select)("core/notices").getNotices,t=Object(i.dispatch)("core/notices").removeNotice;e().filter(function(e){return"amp-errors-notice"===e.id})&&t("amp-errors-notice")},s=[],m=function(){var e,t=Object(i.select)("amp/block-validation"),r=t.getValidationErrors,n=t.isSanitizationAutoAccepted,a=t.getReviewLink,o=Object(i.dispatch)("core/notices").createWarningNotice,c=r(),u=c.length;e=Object(l.sprintf)(
/* translators: %s: number of issues */
Object(l._n)("There is %s issue from AMP validation which needs review.","There are %s issues from AMP validation which need review.",u,"amp"),u);var s=c.filter(function(e){return e.clientId}),m=s.length;if(m>0?e+=" "+Object(l.sprintf)(
/* translators: %s: number of block errors. */
Object(l._n)("%s issue is directly due to content here.","%s issues are directly due to content here.",m,"amp"),m):1===c.length?e+=" "+Object(l.__)("The issue is not directly due to content here.","amp"):e+=" "+Object(l.__)("The issues are not directly due to content here.","amp"),e+=" ",n()){var b=s.filter(function(e){return 0===e.status||2===e.status}),d=c.filter(function(e){return 0===e.status||2===e.status});e+=0===b.length+d.length?Object(l.__)("However, your site is configured to automatically accept sanitization of the offending markup.","amp"):Object(l._n)("Your site is configured to automatically accept sanitization errors, but this error could be from when auto-acceptance was not selected, or from manually rejecting an error.","Your site is configured to automatically accept sanitization errors, but these errors could be from when auto-acceptance was not selected, or from manually rejecting an error.",c.length,"amp")}else e+=Object(l.__)("Non-accepted validation errors prevent AMP from being served, and the user will be redirected to the non-AMP version.","amp");var f={id:"amp-errors-notice"},p=a();p&&(f.actions=[{label:Object(l.__)("Review issues","amp"),url:p}]),o(e,f)},b=r(11),d=r(0),f=(r(5),function(e){var t=e.message,r=e.code,n=e.node_name,a=e.parent_name;return t||("invalid_element"===r&&n?Object(d.createElement)(d.Fragment,null,Object(l.__)("Invalid element: ","amp"),Object(d.createElement)("code",null,n)):"invalid_attribute"===r&&n?Object(d.createElement)(d.Fragment,null,Object(l.__)("Invalid attribute: ","amp"),Object(d.createElement)("code",null,a?Object(l.sprintf)("%s[%s]",a,n):n)):Object(d.createElement)(d.Fragment,null,Object(l.__)("Error code: ","amp"),Object(d.createElement)("code",null,r||Object(l.__)("unknown","amp"))))}),p=r(2),h=r(14),O=Object(i.withSelect)(function(e,t){var r=t.clientId;return{blockValidationErrors:(0,e("amp/block-validation").getBlockValidationErrors)(r)}}),g=Object(h.createHigherOrderComponent)(function(e){return O(function(t){var r=t.blockValidationErrors,n=t.onReplace,a=r.length;if(0===a)return Object(d.createElement)(e,t);var o=[{label:Object(l.__)("Remove Block","amp"),onClick:function(){return n([])}}];return Object(d.createElement)(d.Fragment,null,Object(d.createElement)(p.Notice,{status:"warning",isDismissible:!1,actions:o},Object(d.createElement)("details",{className:"amp-block-validation-errors"},Object(d.createElement)("summary",{className:"amp-block-validation-errors__summary"},Object(l.sprintf)(Object(l._n)("There is %s issue from AMP validation.","There are %s issues from AMP validation.",a,"amp"),a)),Object(d.createElement)("ul",{className:"amp-block-validation-errors__list"},r.map(function(e,t){return Object(d.createElement)("li",{key:t},Object(d.createElement)(f,e))})))),Object(d.createElement)(e,t))})},"withValidationErrorNotice"),v=r(8),j=r.n(v),_=r(31),y=r.n(_);function x(e,t){return{type:"ADD_VALIDATION_ERROR",error:e,clientId:t}}function E(){return{type:"RESET_VALIDATION_ERRORS"}}function k(e){return{type:"UPDATE_REVIEW_LINK",url:e}}function A(e){return e.errors}function w(e,t){return e.errors.filter(function(e){return e.clientId===t})}function S(e){return e.reviewLink}function P(e){return Boolean(e.isSanitizationAutoAccepted)}Object(i.registerStore)("amp/block-validation",{reducer:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:void 0,t=arguments.length>1?arguments[1]:void 0,r=t.type,n=t.url,a=t.error,o=t.clientId;switch(r){case"ADD_VALIDATION_ERROR":var i=e?e.errors:[],c=j()({},a,{clientId:o});return j()({},e,{errors:[].concat(y()(i),[c])});case"RESET_VALIDATION_ERRORS":return j()({},e,{errors:[]});case"UPDATE_REVIEW_LINK":return j()({},e,{reviewLink:n})}return e},selectors:a,actions:n,initialState:j()({},window.ampBlockValidation,{errors:[],reviewLink:void 0})}),r(26);var T=Object(i.select)("core/editor").isEditedPostDirty;Object(i.subscribe)(function(){var e,t;T()||(Object(b.e)()?function(){var e=Object(i.select)("core/block-editor"),t=e.getBlockCount,r=e.getClientIdsWithDescendants,n=e.getBlock,a=Object(i.select)("core/editor").getCurrentPost,o=Object(i.dispatch)("amp/block-validation"),l=o.resetValidationErrors,b=o.addValidationError,d=o.updateReviewLink;if(0!==t()){var f=a(),p=f.amp_validity||{};if(p.results&&p.review_link){var h=p.results.filter(function(e){return 3!==e.term_status}).map(function(e){return e.error});if(!Object(c.isEqual)(h,s))if(s=h,l(),0!==h.length){d(p.review_link);var O=r(),g=!0,v=!1,j=void 0;try{for(var _,y=h[Symbol.iterator]();!(g=(_=y.next()).done);g=!0){var x=_.value;if(!x.sources){b(x);break}var E=void 0,k=!0,A=!1,w=void 0;try{for(var S,P=x.sources[Symbol.iterator]();!(k=(S=P.next()).done);k=!0){var T=S.value;if(T.block_name&&void 0!==T.block_content_index&&f.id===T.post_id){var L=O[T.block_content_index];if(L){var I=n(L);I&&I.name===T.block_name&&(E=L)}}}}catch(e){A=!0,w=e}finally{try{k||null==P.return||P.return()}finally{if(A)throw w}}b(x,E)}}catch(e){v=!0,j=e}finally{try{g||null==y.return||y.return()}finally{if(v)throw j}}m()}else u()}}}():(e=Object(i.select)("amp/block-validation").getValidationErrors,t=Object(i.dispatch)("amp/block-validation").resetValidationErrors,e().length>0&&(t(),u(),s=[])))}),Object(o.addFilter)("editor.BlockEdit","amp/add-notice",g,99)}]);