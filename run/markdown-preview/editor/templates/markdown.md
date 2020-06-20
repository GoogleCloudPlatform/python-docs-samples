# Playing with Markdown

This UI allows a user to write Markdown text and preview the rendered HTML.

You may be familiar with this workflow from sites such as Github or Wikipedia.

In practice, this web page does the following:

* On click of the *"Preview Rendered Markdown"* button, browser JavaScript
  lifts the markdown text and sends it to the editor UI's public backend.
* The editor backend sends the text to a private Renderer service which
  converts it to HTML.
* The HTML is injected into the web page in the right-side **Rendered HTML** area.

## Markdown Background

Markdown is a text-to-HTML conversion tool that allows you to convert plain text to valid HTML.

Read more about the [syntax on Wikipedia](https://en.wikipedia.org/wiki/Markdown).
