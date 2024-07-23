import * as React from "react";
import { useServer } from "./_server";
import * as Layout from "@/pages/_server";


const Home = () => {
  const serverState = useServer();
  const layout = Layout.useServer();

  return (
    <div className="p-6">
      <h1 className="text-2xl">Welcome &lt;{layout.user?.username || "anon"}&gt;</h1>
      <div className="card">
        <ol>
          {serverState.questions.map((question, idx) => (
            <>
              <li key={question.pub_date}><b>{question.question_text}</b></li>
              <ul>
                {question.choices.map((choice, idx) => (
                  <li key={choice.choice_text}>{idx + 1}. {choice.choice_text}</li>
                ))}
              </ul>
            </>
          ))}
        </ol>
        <small>{serverState.questions.length} questions</small>
      </div>
    </div>
  );
};

export default Home;
