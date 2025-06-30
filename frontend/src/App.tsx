import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";
import { Toaster, toast } from "sonner";
import Image from "./components/image";
import QRCode from "./components/qrcode";

interface ApiError {
  message: string;
}

function App() {
  const [text, setText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  // const [isCutting, setIsCutting] = useState(false);

  const handlePrint = async () => {
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
        toast.success("Texte imprimé et coupé avec succès");
      } else {
        const errorData = (await response
          .json()
          .catch(() => null)) as ApiError | null;
        toast.error(
          errorData?.message ||
            `Erreur lors de l'impression (${response.status}): ${response.statusText}`
        );
      }
    } catch (error: unknown) {
      console.error("Print error:", error);
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Erreur de connexion au serveur d'impression";
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  // const handleCut = async () => {
  //   setIsCutting(true);

  //   try {
  //     const response = await fetch("/api/cut", {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify({
  //         text: text,
  //       }),
  //     });

  //     if (response.ok) {
  //       toast.success("Papier coupé avec succès");
  //     } else {
  //       const errorData = (await response
  //         .json()
  //         .catch(() => null)) as ApiError | null;
  //       toast.error(
  //         errorData?.message ||
  //           `Erreur lors de la coupe (${response.status}): ${response.statusText}`
  //       );
  //     }
  //   } catch (error: unknown) {
  //     console.error("Cut error:", error);
  //     const errorMessage =
  //       error instanceof Error
  //         ? error.message
  //         : "Erreur de connexion au serveur";
  //     toast.error(errorMessage);
  //   } finally {
  //     setIsCutting(false);
  //   }
  // };

  return (
    <>
      <Toaster />
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
            disabled={!text.trim() || isLoading}
            className="flex-1/2"
          >
            {isLoading ? "Impression..." : "Imprimer et couper"}
          </Button>
          {/* <Button
            onClick={handleCut}
            disabled={isCutting || isLoading}
            variant="outline"
            className="px-6"
          >
            {isCutting ? "Coupe..." : "Couper"}
          </Button> */}
          <QRCode className="flex-1/4"></QRCode>
          <Image className="flex-1/4"></Image>
        </div>
      </div>
    </>
  );
}

export default App;
