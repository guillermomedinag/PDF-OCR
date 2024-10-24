import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useToast } from "@/components/ui/use-toast";
import { Upload, FileText } from "lucide-react";
import { useState } from "react";

const Index = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const { toast } = useToast();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.type === "application/pdf") {
        setSelectedFile(file);
        toast({
          title: "Archivo cargado",
          description: `${file.name} ha sido seleccionado`,
        });
      } else {
        toast({
          variant: "destructive",
          title: "Error",
          description: "Por favor selecciona un archivo PDF",
        });
      }
    }
  };

  const processDocument = async () => {
    if (!selectedFile) return;

    setIsProcessing(true);
    try {
      // Aquí iría la llamada al backend de Python
      // Por ahora simulamos un delay
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      toast({
        title: "¡Procesamiento completado!",
        description: "El texto ha sido extraído exitosamente",
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Hubo un error al procesar el documento",
      });
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 p-4 sm:p-8">
      <div className="max-w-2xl mx-auto">
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="text-2xl text-center">OCR de Documentos PDF</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex flex-col items-center justify-center p-6 border-2 border-dashed rounded-lg border-gray-300 bg-gray-50 hover:bg-gray-100 transition-colors">
              <Input
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="flex flex-col items-center cursor-pointer"
              >
                <Upload className="h-12 w-12 text-gray-400 mb-2" />
                <span className="text-sm text-gray-600">
                  {selectedFile ? selectedFile.name : "Selecciona un archivo PDF"}
                </span>
              </label>
            </div>

            <Button
              onClick={processDocument}
              disabled={!selectedFile || isProcessing}
              className="w-full"
            >
              <FileText className="mr-2 h-4 w-4" />
              {isProcessing ? "Procesando..." : "Procesar documento"}
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Index;