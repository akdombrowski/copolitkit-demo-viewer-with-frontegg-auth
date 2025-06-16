import { Dispatch, SetStateAction } from "react";
import { useAuth, useAuthUser, useLoginWithRedirect, useAuthActions } from "@frontegg/nextjs";

interface haikuProps {
  generatedHaiku: generate_haiku | Partial<generate_haiku>;
  setHaikus: Dispatch<SetStateAction<generate_haiku[]>>;
  haikus: generate_haiku[];
}

interface generate_haiku {
  japanese: string[] | [];
  english: string[] | [];
  image_names: string[] | [];
  selectedImage: string | null;
}

export default function LoginButton() {
  const login = useLoginWithRedirect;

  return (
    <div className="suggestion-card text-left rounded-md p-4 mt-4 mb-4 flex flex-col bg-gray-100">
      <div className="border-b border-gray-300 mb-4 pb-4">
        <button onSubmit={login}>Login</button>
      </div>
    </div>
  );
}
