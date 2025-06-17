import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

function App() {
  return (
    <div className="h-svh w-full max-w-lg mx-auto flex flex-col gap-3 p-6">
      <h1 className="font-medium">papierpiano</h1>
      <Textarea className="grow" placeholder="Tapez votre texte ici." />
      <Button>Imprimer</Button>
    </div>
  );
}

export default App;
