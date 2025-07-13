import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";
import { toast } from "sonner";

const TextTab = () => {
  const [text, setText] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handlePrint = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("/api/print", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });
      if (response.ok) {
        setText("");
        toast.success("Texte imprimé et coupé avec succès");
      } else {
        const errorData = await response.json().catch(() => null);
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

  return (
    <div className="flex flex-col gap-6 py-4">
      <Textarea
        className="min-h-32 resize-none font-[Courier_New] text-base md:text-base"
        placeholder="Tapez votre texte ici."
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => {
          if (
            (e.ctrlKey || e.metaKey) &&
            e.key === "Enter" &&
            text.trim() &&
            !isLoading
          ) {
            e.preventDefault();
            handlePrint();
          }
        }}
      />
      <div className="flex">
        <Button
          className="flex-1"
          disabled={!text.trim() || isLoading}
          onClick={handlePrint}
        >
          {isLoading ? "Impression..." : "Imprimer et couper"}
        </Button>
      </div>
    </div>
  );
};

export default TextTab;
