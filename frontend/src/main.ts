import App from "./App.svelte";

import "./styles/global.scss";
import "bootstrap";

const app = new App({
  target: document.body,
  props: {},
});

export default app;
