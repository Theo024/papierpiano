import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useState } from "react";
import { toast } from "sonner";

const ImageTab = () => {
  const [imgFile, setImgFile] = useState<File | null>(null);
  const [imgCaption, setImgCaption] = useState("");
  const [imgLoading, setImgLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setImgFile(e.target.files[0]);
    }
  };

  const handleImage = async () => {
    if (!imgFile) {
      toast.error("Veuillez sélectionner une image à imprimer");
      return;
    }
    setImgLoading(true);
    const formData = new FormData();
    formData.append("file", imgFile);
    formData.append("caption", imgCaption);
    try {
      const response = await fetch("/api/image", {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        setImgFile(null);
        setImgCaption("");
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
      setImgLoading(false);
    }
  };

  return (
    <div onSubmit={handleImage} className="flex flex-col gap-6 py-4">
      <div className="grid gap-3">
        <Label htmlFor="image">Image</Label>
        <Input id="image" type="file" onChange={handleFileChange} />
      </div>

      <div className="grid gap-3">
        <Label htmlFor="caption">Légende</Label>
        <Input
          className="font-[Courier_New]"
          id="caption"
          name="caption"
          value={imgCaption}
          onChange={(e) => setImgCaption(e.target.value)}
        />
      </div>

      <div className="flex">
        <Button className="flex-1" disabled={imgLoading} onClick={handleImage}>
          {imgLoading ? "Impression..." : "Imprimer l'image"}
        </Button>
      </div>
    </div>
  );
};

export default ImageTab;
