import {CustomNode} from "./CustomNode";
import {CustomLink} from "./CustomLink";

export interface GraphProps {
    nodes: CustomNode[];
    links: CustomLink[];
}