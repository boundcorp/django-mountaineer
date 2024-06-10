
import React from "react";
import { useServer } from "./_server/useServer";

const Home = () => {
  const serverState = useServer();

  return (
    <div className="p-6">
      <h1 className="text-2xl">Home</h1>
      <div>
        <small>{serverState.questions.length} questions</small>
        <ol>
          {serverState.questions.map((question, idx) => (
            <li key={question.pub_date}>{idx+1}. {question.question_text}</li>
          ))}
        </ol>
      </div>
    </div>
  );
};

export default Home;
