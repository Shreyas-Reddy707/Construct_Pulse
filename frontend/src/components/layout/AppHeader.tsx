import { useAuthStore } from "@/store/useAuthStore";
import { User, LogOut, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export function AppHeader() {
  const { user, clearAuth } = useAuthStore();

  return (
    <header className="flex h-14 items-center justify-between border-b px-4 lg:px-6 bg-background">
      <div className="flex items-center gap-4">
        {/* We can place breadcrumbs or page context here later */}
        <p className="font-semibold text-sm lg:text-base hidden sm:block text-muted-foreground">
          ConstructPulse Workspace
        </p>
      </div>

      <div className="flex items-center gap-4">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-10 pl-2 pr-3 py-2 flex items-center gap-2 hover:bg-accent rounded-full lg:rounded-md">
              <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                <User className="h-4 w-4 text-primary" />
              </div>
              <div className="flex-col items-start hidden lg:flex text-left">
                <span className="text-sm font-medium leading-none">
                  {user?.name || user?.email || "User"}
                </span>
                <span className="text-xs text-muted-foreground mt-1 capitalize leading-none">
                  {user?.role || "Guest"}
                </span>
              </div>
              <ChevronDown className="h-4 w-4 text-muted-foreground hidden lg:block ml-1" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56">
            <DropdownMenuLabel className="font-normal">
              <div className="flex flex-col space-y-1">
                <p className="text-sm font-medium leading-none">{user?.name || "User"}</p>
                <p className="text-xs leading-none text-muted-foreground">
                  {user?.email}
                </p>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem 
              className="text-destructive focus:text-destructive cursor-pointer"
              onClick={() => clearAuth()}
            >
              <LogOut className="mr-2 h-4 w-4" />
              <span>Log out</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}
