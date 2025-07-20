import ImageTab from "@/components/ImageTab";
import QRCodeTab from "@/components/QRCodeTab";
import TextTab from "@/components/TextTab";
import TodoTab from "@/components/todos/TodoTab";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useAtom } from "jotai";
import { atomWithStorage } from "jotai/utils";
import { Toaster } from "sonner";

type Tab = "text" | "todo" | "qrcode" | "image";
const selectedTabAtom = atomWithStorage<Tab>("selectedTab", "text");

function App() {
  const [selectedTab, setSelectedTab] = useAtom(selectedTabAtom);

  return (
    <>
      <Toaster />
      <div className="max-w-[33.5rem] w-full mx-auto flex flex-col gap-3 p-6">
        <h1 className="font-medium">papierpiano</h1>
        <Tabs
          value={selectedTab}
          onValueChange={(v) => setSelectedTab(v as Tab)}
        >
          <TabsList>
            <TabsTrigger value="text">Texte</TabsTrigger>
            <TabsTrigger value="todo">Todo</TabsTrigger>
            <TabsTrigger value="qrcode">QR Code</TabsTrigger>
            <TabsTrigger value="image">Image</TabsTrigger>
          </TabsList>
          <TabsContent value="text">
            <TextTab />
          </TabsContent>
          <TabsContent value="todo">
            <TodoTab />
          </TabsContent>
          <TabsContent value="qrcode">
            <QRCodeTab />
          </TabsContent>
          <TabsContent value="image">
            <ImageTab />
          </TabsContent>
        </Tabs>
      </div>
    </>
  );
}

export default App;
