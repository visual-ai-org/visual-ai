import {EpochObject} from "./EpochObject";
import {WeightObject} from "./WeightObject";

export type NetworkProps = {
    width: number;
    height: number;
    layerPerceptronMap: Map<number, number>;
    weights: WeightObject[]
    epoch: EpochObject[]
};