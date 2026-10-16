
"use client";

import {
  ClerkProvider,
  useAuth,
  useUser,
} from "@clerk/nextjs";
import {
  createContext,
  ReactNode,
  useCallback,
  useContext,
  useMemo,
} from "react";

type PolicyAuth = {
  configured: boolean;
  loaded: boolean;
  signedIn: boolean;
  userId: string | null;
  userName: string | null;
  getToken: () => Promise<string | null>;
};

const anonymousAuth: PolicyAuth = {
  configured: false,
  loaded: true,
  signedIn: false,
  userId: null,
  userName: null,
  getToken: async () => null,
};

const PolicyAuthContext = createContext<PolicyAuth>(anonymousAuth);

function ClerkAuthBridge({ children }: { children: ReactNode }) {
  const { getToken, isLoaded, isSignedIn } = useAuth();
  const { user } = useUser();
  const getAccessToken = useCallback(() => getToken(), [getToken]);

  const value = useMemo<PolicyAuth>(() => ({
    configured: true,
    loaded: isLoaded,
    signedIn: Boolean(isSignedIn),
    userId: user?.id ?? null,
    userName: user?.fullName ?? user?.primaryEmailAddress?.emailAddress ?? null,
    getToken: getAccessToken,
  }), [getAccessToken, isLoaded, isSignedIn, user?.id, user?.fullName, user?.primaryEmailAddress?.emailAddress]);

  return (
    <PolicyAuthContext.Provider value={value}>
      {children}
    </PolicyAuthContext.Provider>
  );
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const publishableKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;

  if (!publishableKey) {
    return (
      <PolicyAuthContext.Provider value={anonymousAuth}>
        {children}
      </PolicyAuthContext.Provider>
    );
  }

  return (
    <ClerkProvider publishableKey={publishableKey}>
      <ClerkAuthBridge>{children}</ClerkAuthBridge>
    </ClerkProvider>
  );
}

export function usePolicyAuth() {
  return useContext(PolicyAuthContext);
}
