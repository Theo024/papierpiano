import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { useState } from "react";
import { toast } from "sonner";

const QRCodeTab = () => {
  const [qrContent, setQrContent] = useState("");
  const [qrSize, setQrSize] = useState([16]);
  const [qrLoading, setQrLoading] = useState(false);

  const handleQRCode = async () => {
    if (!qrContent.trim()) {
      toast.error("Veuillez saisir du contenu pour le QR Code");
      return;
    }
    setQrLoading(true);
    try {
      const response = await fetch("/api/qrcode", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content: qrContent,
          size: qrSize[0],
        }),
      });
      if (response.ok) {
        setQrContent("");
        toast.success("QR Code imprimé avec succès");
      } else {
        const errorData = await response.json().catch(() => null);
        toast.error(
          errorData?.message ||
            `Erreur lors de l'impression du QR Code (${response.status}): ${response.statusText}`
        );
      }
    } catch (error: unknown) {
      console.error("QRCode request error:", error);
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Erreur de connexion au serveur";
      toast.error(errorMessage);
    } finally {
      setQrLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-6 py-4">
      <div className="grid gap-3">
        <Label htmlFor="content">Contenu</Label>
        <Input
          id="content"
          name="content"
          value={qrContent}
          onChange={(e) => setQrContent(e.target.value)}
        />
      </div>

      <div className="grid gap-3">
        <div className="flex items-center justify-between">
          <Label htmlFor="size">Taille</Label>
          <span className="text-sm font-medium">{qrSize[0]}</span>
        </div>
        <Slider
          id="size"
          name="size"
          min={1}
          max={16}
          step={1}
          value={qrSize}
          onValueChange={setQrSize}
          className="w-full mb-2"
        />
      </div>

      <div className="flex">
        <Button className="flex-1" disabled={qrLoading} onClick={handleQRCode}>
          {qrLoading ? "Impression..." : "Imprimer le QR Code"}
        </Button>
      </div>
    </div>
  );
};

export default QRCodeTab;
