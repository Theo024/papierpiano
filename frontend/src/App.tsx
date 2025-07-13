import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Toaster } from "sonner";

import ImageTab from "@/components/tabs/ImageTab";
import QRCodeTab from "@/components/tabs/QRCodeTab";
import TextTab from "@/components/tabs/TextTab";
import TodoTab from "@/components/tabs/TodoTab";
import { useState } from "react";

function App() {
  const [mode, setMode] = useState<"text" | "todo" | "qrcode" | "image">(
    "text"
  );

  return (
    <>
      <Toaster />
      <div
        className="max-w-[33.5rem] w-full mx-auto flex flex-col gap-3 p-6"
        // style={{
        //   width:
        //     "calc(48ch + 2px + 1px + var(--spacing) * 6 + var(--spacing) * 6)",
        // }}
      >
        <h1 className="font-medium">papierpiano</h1>
        <Tabs
          value={mode}
          onValueChange={(v) =>
            setMode(v as "text" | "todo" | "qrcode" | "image")
          }
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
