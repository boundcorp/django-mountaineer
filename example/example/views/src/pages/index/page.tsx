import * as React from "react";
import * as HomeController from "./_server";
import * as Layout from "@/pages/_server";
import { Dialog, Transition } from '@headlessui/react';
import { useForm, useFieldArray } from 'react-hook-form';
import { handleFormSubmit } from "@/components/utils";
import { createServerPage } from "@/components/ServerPages";
import { LayoutPage } from "../layout";

const HomePage = createServerPage(HomeController);


const CreateQuestionModal = ({ closeModal }: { closeModal: () => void }) => {
  const {create} = HomePage.useContext();
  const form = useForm({
    defaultValues: {
      question_text: '',
      choices: [{ choice_text: '' }]
    }
  });
  const { register, control, handleSubmit } = form;
  const { fields, append, remove } = useFieldArray({
    control,
    name: 'choices'
  });

  return (
    <form onSubmit={handleFormSubmit(form, async (data) => {
      await create({ requestBody: { question_text: data.question_text, choices: data.choices.map(choice => choice.choice_text) } });
      closeModal();
    })}>
      <div className="form-control mb-4">
        <label className="label">
          <span className="label-text">Question Text</span>
        </label>
        <input {...register('question_text')} className="input input-bordered" />
      </div>
      <fieldset className="form-control mb-4">
        <legend className="label-text mb-2">Choices</legend>
        {fields.map((item, index) => (
          <div key={item.id} className="flex items-center mb-2">
            <input {...register(`choices.${index}.choice_text`)} className="input input-bordered flex-grow mr-2" />
            <button type="button" onClick={() => remove(index)} className="btn btn-error">Remove</button>
          </div>
        ))}
        <button type="button" onClick={() => append({ choice_text: '' })} className="btn btn-secondary">Add Choice</button>
      </fieldset>
      <button type="submit" className="btn btn-primary">Create</button>
    </form>
  );
};

const Home = () => {
  const {questions, create, vote, clear} = HomePage.useContext();
  const {user} = LayoutPage.useContext();
  const [isOpen, setIsOpen] = React.useState(false);

  const openModal = () => setIsOpen(true);
  const closeModal = () => setIsOpen(false);

  return (
      <div className="p-6">
        <h1 className="text-2xl">Welcome &lt;{user?.username || "anon"}&gt;</h1>
        <div className="card">
          <button className="btn btn-secondary" onClick={() => clear()}>Clear</button>
          <button className="btn btn-primary" onClick={openModal}>Create Question</button>
          <Transition appear show={isOpen} as={React.Fragment}>
            <Dialog as="div" className="relative z-10" onClose={closeModal}>
              <Transition.Child
                as={React.Fragment}
                enter="ease-out duration-300"
                enterFrom="opacity-0"
                enterTo="opacity-100"
                leave="ease-in duration-200"
                leaveFrom="opacity-100"
                leaveTo="opacity-0"
              >
                <div className="fixed inset-0 bg-black bg-opacity-25" />
              </Transition.Child>

              <div className="fixed inset-0 overflow-y-auto">
                <div className="flex min-h-full items-center justify-center p-4 text-center">
                  <Transition.Child
                    as={React.Fragment}
                    enter="ease-out duration-300"
                    enterFrom="opacity-0 scale-95"
                    enterTo="opacity-100 scale-100"
                    leave="ease-in duration-200"
                    leaveFrom="opacity-100 scale-100"
                    leaveTo="opacity-0 scale-95"
                  >
                    <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-gray-800 p-6 text-left align-middle shadow-xl transition-all">
                      <Dialog.Title as="h3" className="text-lg font-medium leading-6 text-white">
                        Create a new question
                      </Dialog.Title>
                      <CreateQuestionModal closeModal={closeModal}/>
                    </Dialog.Panel>
                  </Transition.Child>
                </div>
              </div>
            </Dialog>
          </Transition>
          <ol>
            {questions.map((question, idx) => (
              <div key={question.pub_date}>
                <li><b>{question.question_text}</b></li>
                <ul>
                  {question.choices.map((choice, idx) => (
                    <li key={choice.choice_text} className="p-1">
                      <button className="ml-2 btn btn-primary btn-sm" onClick={() => question?.id && choice?.id && vote({ question_id: question.id, choice_id: choice.id })}>Vote</button>
                      &nbsp; {choice.choice_text} ({choice.votes} votes)
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </ol>
          <small>{questions.length} questions</small>
        </div>
      </div>
  );
};

export default HomePage.wraps(Home);
