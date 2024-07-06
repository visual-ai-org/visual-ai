interface Perceptron {
    weights: number[];
    bias: number;
}

interface Layer {
    [key: string]: Perceptron;
}

interface Weights {
    [key: string]: Layer;
}

interface Data {
    type: "weights";
    weights: Weights;
}

interface WeightObject {
    data: Data;
}
