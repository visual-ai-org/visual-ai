import {CustomNode} from "./CustomNode";

export interface CustomLink {
    source: CustomNode;
    target: CustomNode;
    value: Number;
    sourceLayer: Number;
    targetLayer: Number;
    sourceIndex: Number;
    targetIndex: Number;
}
