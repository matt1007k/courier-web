import styled from "styled-components";

interface ProgressContentProps {
  percentage: number;
}
export const ProgressContainer = styled.div`
  height: 15px;
  width: 100%;
  background-color: var(--btn-default-color);
  border-radius: 4px;
  position: relative;
  overflow: hidden;
`;

export const ProgressContent = styled.div<ProgressContentProps>`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: ${(props) => props.percentage + "%"};
  color: ${(props) => (props.percentage >= 50 ? "white" : "black")};
  background-color: rgba(var(--primary-page-color));
  transition: width 0.6s cubic-bezier(0.165, 0.84, 0.44, 1) ease-in;
`;
