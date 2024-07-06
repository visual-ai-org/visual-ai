export type NetworkProps = {
    width: number;
    height: number;
    layerPerceptronMap: Map<number, number>;
    weights: WeightObject[]
    epoch: EpochObject[]
};