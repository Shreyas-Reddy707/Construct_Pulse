import { FileText } from "lucide-react";

export function WorkerDocumentsTab() {
  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-semibold tracking-tight text-lg">Documents & Certifications</h3>
        <p className="text-sm text-muted-foreground">
          OSHA cards, medical clearances, and site inductions.
        </p>
      </div>

      <div className="bg-card shadow-sm border rounded-xl overflow-hidden py-16 flex flex-col items-center justify-center text-center space-y-4">
        <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center text-muted-foreground">
          <FileText className="w-8 h-8" />
        </div>
        <div className="max-w-sm">
          <h4 className="font-medium text-lg">No documents uploaded</h4>
          <p className="text-sm text-muted-foreground mt-1">
            Certifications and OSHA cards will appear here in a future update.
          </p>
        </div>
      </div>
    </div>
  );
}
