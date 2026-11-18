import { createApp } from "./app";
import { d1Store } from "./notes";

export default createApp((env) => d1Store(env.DB));
