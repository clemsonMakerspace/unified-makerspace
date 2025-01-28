// getAmplifyConfig.ts

interface AmplifyConfig {
  userPoolId: string;
  userPoolClientId: string;
}

export function getAmplifyConfig(): AmplifyConfig {
  const hostname = window.location.hostname;

  const prodUserPoolId = "us-east-1_TQ9FwRJ44";
  const prodUserPoolClientId = "58lututlkaggp6h8tu9oauqp5p";

  const betaUserPoolId = "us-east-1_4w535EQDB";
  const betaUserPoolClientId = "6sfun4otg8chqplrmco2qvivni";

  if (hostname === "visit.cumaker.space") {
    console.log("prod env");
    return {
      userPoolId: prodUserPoolId,
      userPoolClientId: prodUserPoolClientId,
    };
  } else if (hostname === "beta-visit.cumaker.space") {
    console.log("beta env");
    return {
      userPoolId: betaUserPoolId,
      userPoolClientId: betaUserPoolClientId,
    };
  } else {
    // Default to beta
    console.log("default env");
    return {
      userPoolId: betaUserPoolId,
      userPoolClientId: betaUserPoolClientId,
    };
  }
}
