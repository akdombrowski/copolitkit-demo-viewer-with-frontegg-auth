"use client";

import { DoorClosedLocked, DoorOpen } from "lucide-react";
import { useTheme } from "next-themes";

import { Button } from "@/components/ui/button";

export function LoginButton() {
  const { theme, setTheme } = useTheme();

  return (
    <Button
      variant="default"
      size="sm"
      onClick={() => setTheme(theme === "light" ? "dark" : "light")}
      className="h-8 w-8 px-0"
    >
      <DoorOpen className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <DoorClosedLocked className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Login</span>
    </Button>
  );
}
