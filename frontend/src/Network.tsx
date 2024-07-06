import React, {useEffect, useState} from "react";
import {DefaultNode, Graph} from "@visx/network";
import {NetworkProps} from "./interface/NetworkProps";
import {addLayer, remove_layer} from "./api";

type PerceptronWeights = {
  bias: number;
  weights: number[];
};

type LayerWeights = {
  [key: string]: PerceptronWeights;
};

type Weights = {
  [key: string]: LayerWeights;
};

const setBackend = async (layerPerceptronMap: Map<number, number>) => {
  let r;
  for (const [layer, perceptrons] of layerPerceptronMap.entries()) {
    r = addLayer(perceptrons, "sigmoid")
  }
  return r
}

const resetBackend = async () => {
  for (let i = 0; i < 100; i++) {
    try {
      const res = await remove_layer();
      if (res.message === "Layer is empty") {
        break;
      }
    } catch (error) {
      console.error('Error removing layer:', error);
    }
  }
}

const updateEdgeValue = (edges: CustomLink[], weights: Weights): CustomLink[] => {
  return edges.map(edge => {
    const sourceLayer = Number(edge.sourceLayer);
    const targetLayer = Number(edge.targetLayer);
    const sourceIndex = edge.sourceIndex;

    // Form the keys for the source layer and perceptron
    const sourceLayerKey = `layer ${sourceLayer}`;
    const targetLayerKey = `layer ${targetLayer}`;
    const perceptronKey = `perceptron ${sourceIndex}`;

    // Log the keys to debug
    console.log(`sourceLayerKey: ${sourceLayerKey}, targetLayerKey: ${targetLayerKey}, perceptronKey: ${perceptronKey}`);

    // Check if the keys exist
    if (weights[sourceLayerKey] && weights[sourceLayerKey][perceptronKey]) {
      const perceptronWeights = weights[sourceLayerKey][perceptronKey].weights;
      const weightIndex = targetLayer - sourceLayer - 1;

      // Log the weightIndex to debug
      console.log(`weightIndex: ${weightIndex}, perceptronWeights: ${perceptronWeights}`);

      // Check if the weight index is valid
      if (weightIndex >= 0 && weightIndex < perceptronWeights.length) {
        const weightValue = perceptronWeights[weightIndex];
        return { ...edge, value: weightValue };
      } else {
        console.error(`Invalid weight index: ${weightIndex} for sourceLayer ${sourceLayer}, targetLayer ${targetLayer}`);
      }
    } else {
      console.error(`Invalid keys: sourceLayerKey = ${sourceLayerKey}, targetLayerKey = ${targetLayerKey}, perceptronKey = ${perceptronKey}`);
    }

    // Return edge with default value if there was an error
    return { ...edge, value: 0 };
  });
};

export default function Network({
  width,
  height,
  layerPerceptronMap,
}: NetworkProps) {

  // TODO: figure out how to store the links and nodes from the map
  const [nodes, setNodes] = useState<CustomNode[]>([]);
  const [edges, setEdges] = useState<CustomLink[]>([]);
  const [graph, setGraph] = useState<GraphProps>();

  const getNodes = (layerPerceptronMap: Map<number, number>) => {
    const result: CustomNode[] = [];
    var x: number = 100;

    for (const [layer, perceptrons] of layerPerceptronMap.entries()) {
      var y = 600 / (perceptrons + 1)
      var interval = 600 / (perceptrons + 1)
      for (let i = 0; i < perceptrons; i++) {
        const node: CustomNode = { x: x, y: y, value: 1, layer: layer, index: i };
        result.push(node);
        y += interval;
      }
      x += 150;
    }
    return result;
  };

  const getEdges = (layerPerceptronMap: Map<number, number>, nodes: CustomNode[]) => {
    const result: CustomLink[] = [];
    const layerPerceptrons = Array.from(layerPerceptronMap.entries());

    var prevLayerNumNodes = layerPerceptrons[0][1];
    var prevLayer = nodes.slice(0, prevLayerNumNodes);
    var offset = prevLayerNumNodes;

    for (let i = 1; i < layerPerceptrons.length; i++) {
      const nextLayerNumNodes = layerPerceptrons[i][1];
      const nextLayer = nodes.slice(offset, offset + nextLayerNumNodes);

      for (const source of prevLayer) {
        for (const target of nextLayer) {
          const newLink: CustomLink = {
            source: source,
            target: target,
            value: 1,
            sourceLayer: source.layer,
            targetLayer: target.layer,
            sourceIndex: source.index,
            targetIndex: target.index
          };
          result.push(newLink);
        }
      }
      offset += nextLayerNumNodes;
      prevLayer = nextLayer;
    }
    return result;
  }

  useEffect(() => {
    const nodes = getNodes(layerPerceptronMap);
    setNodes(nodes);
    setEdges(getEdges(layerPerceptronMap, nodes));
  }, [layerPerceptronMap]);

  useEffect(() => {
    resetBackend().then(r =>
        setBackend(layerPerceptronMap).then(
            r => setEdges(updateEdgeValue(edges, r.weights))
        )
    )
  }, [layerPerceptronMap]);

  useEffect(() => {
    setGraph({nodes: nodes, links: edges});
  }, [layerPerceptronMap, nodes]);

  return width < 10 ? null : (
    <svg width={width} height={height}>
      <Graph<CustomLink, CustomNode>
        graph={graph}
        top={30}
        left={100}
        nodeComponent={({ node: { value } }) => (
          <g>
            <DefaultNode r={20} />
            <text textAnchor="middle"> {value} </text>
          </g>
        )}
        linkComponent={({ link: { source, target } }) => (
          <line
            x1={source.x}
            y1={source.y}
            x2={target.x}
            y2={target.y}
            strokeWidth={2}
            stroke="#999"
            strokeOpacity={0.6}
            // strokeDasharray={dashed ? '8,4' : undefined}
          />
        )}
      />
    </svg>
  );
}
