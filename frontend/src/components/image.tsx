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
import { useState, type FormEvent } from "react";
import { toast } from "sonner";

interface ImageProps {
  className?: string;
}

function Image({ className }: ImageProps) {
  const [open, setOpen] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [caption, setCaption] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleImage = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!file) {
      toast.error("Veuillez sélectionner une image à imprimer");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("caption", caption);

    try {
      const response = await fetch("/api/image", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        setFile(null);
        setOpen(false);
        toast.success("Image imprimée avec succès");
      } else {
        const errorData = await response.json().catch(() => null);
        toast.error(
          errorData?.message ||
            `Erreur lors de l'impression de l'image (${response.status}): ${response.statusText}`
        );
      }
    } catch (error: unknown) {
      console.error("Image request error:", error);
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Erreur de connexion au serveur";
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className={className} variant="outline">
          Image
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <form onSubmit={handleImage}>
          <DialogHeader>
            <DialogTitle>Imprimer une image</DialogTitle>
          </DialogHeader>
          <div className="grid gap-6 py-4">
            <div className="grid gap-3">
              <Label htmlFor="image">Image</Label>
              <Input id="image" type="file" onChange={handleFileChange} />
            </div>
            <div className="grid gap-3">
              <Label htmlFor="caption">Légende</Label>
              <Input
                id="caption"
                name="caption"
                value={caption}
                onChange={(e) => setCaption(e.target.value)}
              />
            </div>
          </div>
          <DialogFooter>
            <DialogClose asChild>
              <Button variant="outline">Cancel</Button>
            </DialogClose>
            <Button type="submit" disabled={loading}>
              {loading ? "Impression..." : "Imprimer"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}

export default Image;
