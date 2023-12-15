// getAmplifyConfig.ts

interface AmplifyConfig {
  userPoolId: string;
  userPoolClientId: string;
}

export function getAmplifyConfig(): AmplifyConfig {
  const hostname = window.location.hostname;

  if (hostname === "visit.cumaker.space") {
    console.log("prod env");
    return {
      userPoolId: "us-east-1_TQ9FwRJ44",
      userPoolClientId: "58lututlkaggp6h8tu9oauqp5p",
    };
  } else if (hostname === "beta-visit.cumaker.space") {
    console.log("beta env");
    return {
      userPoolId: "us-east-1_FXu4qDv8B",
      userPoolClientId: "5rcrlv4el312ht5gos31v0u0n6",
    };
  } else {
    // Default to production
    console.log("default env");
    return {
      userPoolId: "us-east-1_TQ9FwRJ44",
      userPoolClientId: "58lututlkaggp6h8tu9oauqp5p",
    };
  }
}
