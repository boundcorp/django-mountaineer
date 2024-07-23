import * as React from "react";
import {useServer} from "./_server";
import * as Layout from "@/pages/_server";

import "@/main.css"

const Home = () => {
  const serverState = useServer();
  const layout = Layout.useServer();

  return (
    <div className="p-6">
      <h1 className="text-2xl">Welcome &lt;{layout.user?.username || "anon"}&gt;</h1>
      <div className="card">
        <small>{serverState.questions.length} questions</small>
        <ol>
          {serverState.questions.map((question, idx) => (
            <li key={question.pub_date}>{idx + 1}. {question.question_text}</li>
          ))}
        </ol>
      </div>
    </div>
  );
};

export default Home;
