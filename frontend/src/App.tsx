import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { Textarea } from "@/components/ui/textarea";
import { useState, type FormEvent } from "react";

function App() {
  const [text, setText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isCutting, setIsCutting] = useState(false);

  const [open, setOpen] = useState(false);
  const [content, setContent] = useState("");
  const [size, setSize] = useState([3]);

  const handlePrint = async () => {
    if (!text.trim()) return;

    const lines = text.split("\n");
    const wrappedLines = [];

    for (const line of lines) {
      if (line.length <= 48) {
        wrappedLines.push(line);
      } else {
        // Split long lines into chunks of 48 characters
        const chunks = [];
        for (let i = 0; i < line.length; i += 48) {
          chunks.push(line.slice(i, i + 48));
        }
        wrappedLines.push(...chunks);
      }
    }

    const wrappedText = wrappedLines.join("\n");

    setIsLoading(true);

    try {
      const response = await fetch("/api/print", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: wrappedText,
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

  const handleQRCode = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!content.trim()) return;

    try {
      const response = await fetch("/api/qrcode", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content: content,
          size: size[0],
        }),
      });

      if (response.ok) {
        setContent("");
        setOpen(false);
      } else {
        console.error("QRCode request failed:", response.status);
      }
    } catch (error) {
      console.error("QRCode request error:", error);
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
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild>
            <Button variant="outline">QRCode</Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px]">
            <form onSubmit={handleQRCode}>
              <DialogHeader>
                <DialogTitle>QRCode</DialogTitle>
              </DialogHeader>
              <div className="grid gap-6 py-4">
                <div className="grid gap-3">
                  <Label htmlFor="content">Contenu</Label>
                  <Input
                    id="content"
                    name="content"
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                  />
                </div>
                <div className="grid gap-3">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="size">Taille</Label>
                    <span className="text-sm font-medium">{size[0]}</span>
                  </div>
                  <Slider
                    id="size"
                    name="size"
                    min={1}
                    max={16}
                    step={1}
                    value={size}
                    onValueChange={setSize}
                    className="w-full"
                  />{" "}
                </div>
              </div>
              <DialogFooter>
                <DialogClose asChild>
                  <Button variant="outline">Cancel</Button>
                </DialogClose>
                <Button type="submit">Imprimer</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
}

export default App;
