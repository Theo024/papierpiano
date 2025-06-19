import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handlePrint = async () => {
    if (!text.trim()) return;

    setIsLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/print", {
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

  return (
    <div className="h-svh w-full max-w-lg mx-auto flex flex-col gap-3 p-6">
      <h1 className="font-medium">papierpiano</h1>
      <Textarea
        className="grow"
        placeholder="Tapez votre texte ici."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <Button onClick={handlePrint} disabled={!text.trim() || isLoading}>
        {isLoading ? "Impression..." : "Imprimer"}
      </Button>
    </div>
  );
}

export default App;
