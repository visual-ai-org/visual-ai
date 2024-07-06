export interface Perceptron {
    weights: number[];
    bias: number;
}

interface Layer {
    [key: string]: Perceptron;
}

export interface Weights {
    [key: string]: Layer;
}

interface Data {
    type: "weights";
    weights: Weights;
}

export interface WeightObject {
    data: Data;
}
