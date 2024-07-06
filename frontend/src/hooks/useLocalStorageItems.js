import { useEffect, useState } from "react";

function getLocalStorageItems() {
  const items = [];
  const layerInfo = localStorage.getItem("layers");
  var layerObject = JSON.parse(layerInfo);
  if (layerObject == null) {
    // for new users, start with 2 layers by default
    layerObject = {1: 1, 2: 1};
    const newLayerInfo = JSON.stringify(layerObject);
    localStorage.setItem("layers", newLayerInfo);
  }
  for (const [layer, perceptrons] of Object.entries(layerObject)) {
    items.push({ layer, perceptrons });
  }
  console.log(items);
  return items;
}

export default function useLocalStorageItems() {
  const [items, setItems] = useState(getLocalStorageItems());

  useEffect(() => {
    const handleStoreChange = () => {
      setItems(getLocalStorageItems());
    };

    window.addEventListener("storage", handleStoreChange);

    return () => {
      window.removeEventListener("storage", handleStoreChange);
    };
  }, []);

  const map = new Map();
  // console.log("items", items)
  for (const item of items) {
    map.set(item.layer, item.perceptrons)
  }

  return map;
}
