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
      userPoolId: "us-east-1_7a59HeiH9",
      userPoolClientId: "2f3ta1jhat9vpct10pvr7t8f3q",
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
