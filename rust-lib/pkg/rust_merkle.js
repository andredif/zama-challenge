import * as wasm from "./rust_merkle_bg.wasm";
import { __wbg_set_wasm } from "./rust_merkle_bg.js";
__wbg_set_wasm(wasm);
export * from "./rust_merkle_bg.js";
