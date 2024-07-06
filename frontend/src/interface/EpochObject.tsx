export interface EpochObject {
    data: {
        type: "loss";
        epoch: number;
        max_epoch: number;
        loss: number;
    };
}
