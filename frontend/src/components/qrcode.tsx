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
import { useState, type FormEvent } from "react";
import { toast } from "sonner";

interface QRCodeProps {
  className?: string;
}

function QRCode({ className }: QRCodeProps) {
  const [open, setOpen] = useState(false);
  const [content, setContent] = useState("");
  const [size, setSize] = useState([3]);

  const handleQRCode = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!content.trim()) {
      toast.error("Veuillez saisir du contenu pour le QRCode");
      return;
    }

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
        toast.success("QRCode imprimé avec succès");
      } else {
        const errorData = await response.json().catch(() => null);
        toast.error(
          errorData?.message ||
            `Erreur lors de l'impression du QRCode (${response.status}): ${response.statusText}`
        );
      }
    } catch (error: unknown) {
      console.error("QRCode request error:", error);
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Erreur de connexion au serveur";
      toast.error(errorMessage);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className={className} variant="outline">
          QRCode
        </Button>
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
  );
}

export default QRCode;
