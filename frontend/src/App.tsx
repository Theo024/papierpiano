import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";
import Image from "./components/image";
import QRCode from "./components/qrcode";

function App() {
  const [text, setText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isCutting, setIsCutting] = useState(false);

  const handlePrint = async () => {
    if (!text.trim()) return;

    setIsLoading(true);

    try {
      const response = await fetch("/api/print", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: text,
        }),
      });

      if (response.ok) {
        setText(""); // Clear textarea on success
      } else {
        console.error("Print request failed:", response.status);
      }
    } catch (error) {
      console.error("Print request error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCut = async () => {
    setIsCutting(true);

    try {
      const response = await fetch("/api/cut", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: text,
        }),
      });

      if (!response.ok) {
        console.error("Cut request failed:", response.status);
      }
    } catch (error) {
      console.error("Cut request error:", error);
    } finally {
      setIsCutting(false);
    }
  };

  return (
    <div
      className="h-svh w-full mx-auto flex flex-col gap-3 p-6 text-base md:text-base"
      style={{
        width:
          "calc(48ch + 2px + 1px + var(--spacing) * 6 + var(--spacing) * 6)",
      }}
    >
      <h1 className="font-medium">papierpiano</h1>
      <Textarea
        className="grow resize-none font-[Courier_New] text-base md:text-base"
        placeholder="Tapez votre texte ici."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <div className="flex gap-2">
        <Button
          onClick={handlePrint}
          disabled={!text.trim() || isLoading || isCutting}
          className="grow"
        >
          {isLoading ? "Impression..." : "Imprimer"}
        </Button>
        <Button
          onClick={handleCut}
          disabled={isCutting || isLoading}
          variant="outline"
          className="px-6"
        >
          {isCutting ? "Coupe..." : "Couper"}
        </Button>
        <QRCode></QRCode>
        <Image></Image>
      </div>
    </div>
  );
}

export default App;
