import { FileText, FolderOpen } from "lucide-react";

export default function DepartmentDocumentsTab() {
  return (
    <div className="space-y-4">
      <div>
        <h3 className="font-semibold tracking-tight text-lg flex items-center gap-2">
          <FileText className="h-5 w-5 text-primary" />
          Department Documentation
        </h3>
        <p className="text-sm text-muted-foreground">
          SOPs, Work Instructions, Safety Procedures, and Templates.
        </p>
      </div>

      <div className="bg-card border rounded-xl py-20 flex flex-col items-center justify-center text-center space-y-4">
        <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center text-primary">
          <FolderOpen className="w-8 h-8" />
        </div>
        <div className="max-w-md px-4">
          <h4 className="font-medium text-lg">Knowledge Repository</h4>
          <p className="text-sm text-muted-foreground mt-2">
            The department-level document repository is scheduled for a future release. 
            This module will securely host Standard Operating Procedures (SOPs), specialized training material, department-wide work instructions, and official templates for internal distribution.
          </p>
        </div>
      </div>
    </div>
  );
}
