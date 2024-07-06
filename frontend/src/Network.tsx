import React, { useEffect, useState } from "react";
import { DefaultNode, Graph } from "@visx/network";
import {NetworkProps} from "./interface/NetworkProps";
import {addLayer, remove_layer} from "./api";

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

const updateNodeValue = (nodes: CustomNode[], weights: any) => {
    console.log("weights", weights)
    return nodes.map(node => {
        node.value = 1;
        return node;
    });
}

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
    var y: number = 20;
    for (const [layer, perceptrons] of layerPerceptronMap.entries()) {
      for (let i = 0; i < perceptrons; i++) {
        const node: CustomNode = { x: x, y: y, value: 1 };
        result.push(node);
        y += 100;
      }
      x += 150;
      y = 20;
    }
    return result;
  };

  const getEdges = (layerPerceptronMap: Map<number, number>,  nodes: CustomNode[]) => {
    const result: CustomLink[] = [];
    // calculate the number of perceptrons in each layer
    // console.log(layerPerceptronMap)
    // console.log(layerPerceptronMap.entries())
    const layerPerceptrons = Array.from(layerPerceptronMap.entries())
    // console.log(layerPerceptrons)
    var prevLayerNumNodes = layerPerceptrons[0][1]
    // console.log("prev layer number", prevLayerNumNodes)
    var prevLayer = nodes.slice(0, prevLayerNumNodes)
    // console.log("prevLayer", prevLayer)
    var offset = prevLayerNumNodes
    for (let i = 1; i < layerPerceptrons.length; i++) {
      const nextLayerNumNodes = layerPerceptrons[i][1]
      // console.log("next layer num", nextLayerNumNodes)
      const nextLayer = nodes.slice(offset, offset + nextLayerNumNodes)
      // console.log("next layer", nextLayer)

      // form the links
      for (const source of prevLayer) {
        for (const target of nextLayer) {
          const newLink: CustomLink = {source: source, target: target}
          result.push(newLink)
        }
        // console.log("layer connection", result)
      }
      // update the offset and make previous layer become next layer
      offset += nextLayerNumNodes
      // prevLayerNumNodes = nextLayerNumNodes
      prevLayer = nextLayer
    }
    return result
  }

  useEffect(() => {
    // Set Nodes
    setNodes(getNodes(layerPerceptronMap))
    setEdges(getEdges(layerPerceptronMap, nodes))
    console.log("edges", edges)
    setGraph({nodes: nodes, links: edges})
  }, [layerPerceptronMap, nodes, edges]);

  useEffect(() => {
    resetBackend().then(r =>
        setBackend(layerPerceptronMap).then(
            r => updateNodeValue(nodes, r.weights)
        )
    )
  }, [layerPerceptronMap]);

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
