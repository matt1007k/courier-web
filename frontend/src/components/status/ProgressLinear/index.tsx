import React, { ReactElement } from "react";
import { ProgressContainer, ProgressContent } from "./styles";

interface Props {
  percentage: number;
}

function ProgressLinear({ percentage }: Props): ReactElement {
  return (
    <ProgressContainer>
      <ProgressContent percentage={percentage}>{percentage}%</ProgressContent>
    </ProgressContainer>
  );
}

export default ProgressLinear;
