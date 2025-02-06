// getAmplifyConfig.ts

interface AmplifyConfig {
  userPoolId: string;
  userPoolClientId: string;
}

export function getAmplifyConfig(): AmplifyConfig {
  const hostname = window.location.hostname;

  const prodUserPoolId = "us-east-1_biYxbm7Xf";
  const prodUserPoolClientId = "1te4t5qtohl5t0c35lfcsl8vkr";

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
