import * as React from "react";
import * as HomeController from "./_server";
import { Dialog, Menu, MenuButton, MenuItem, MenuItems, Transition } from '@headlessui/react';
import { useForm, useFieldArray } from 'react-hook-form';
import { handleFormSubmit } from "@/components/utils";
import { createServerPage } from "@/components/ServerPages";
import { LayoutPage } from "../layout";
import { EnumPublicChoices } from "@/enums";

const HomePage = createServerPage(HomeController);


const CreateQuestionModal = ({ closeModal }: { closeModal: () => void }) => {
  const { create } = HomePage.useContext();
  const form = useForm({
    defaultValues: {
      question_text: '',
      publicity: EnumPublicChoices.public.value,
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
      await create({ requestBody: { question_text: data.question_text, choices: data.choices.map(choice => choice.choice_text), publicity: data.publicity as HomeController.PublicChoices } });
      closeModal();
    })}>
      <div className="form-control mb-4">
        <label className="label">
          <span className="label-text">Question Text</span>
        </label>
        <input {...register('question_text')} className="input input-bordered" />
      </div>
      <div className="form-control mb-4">
        <label className="label">
          <span className="label-text">Publicity</span>
        </label>
        <select {...register('publicity')} className="select select-bordered">
          {Object.values(EnumPublicChoices).map((option) => (
            <option key={option.value} value={option.value}>{option.label}</option>
          ))}
        </select>
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
  const { questions, create, vote, clear } = HomePage.useContext();
  const { user } = LayoutPage.useContext();
  const [isOpen, setIsOpen] = React.useState(false);

  const openModal = () => setIsOpen(true);
  const closeModal = () => setIsOpen(false);

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl">Welcome &lt;{user?.username || "anon"}&gt;</h1>
        <Menu as="div" className="relative">
          <MenuButton className="btn btn-secondary">
            {questions.length} questions <span className="ml-2">&#9662;</span>
          </MenuButton>
          <MenuItems className="absolute right-0 mt-2 w-48 bg-white shadow-lg z-10 rounded-md">
            <MenuItem>
              <button
                className="block w-full text-left px-4 py-2 text-sm text-gray-700 rounded-md"
                onClick={openModal}
              >
                Create Question
              </button>
            </MenuItem>
            <MenuItem>
              <button
                className="block w-full text-left px-4 py-2 text-sm text-gray-700 rounded-md"
                onClick={() => {
                  if (confirm("Are you sure you want to clear all questions?")) {
                    clear();
                  }
                }}
              >
                Clear Questions
              </button>
            </MenuItem>
          </MenuItems>
        </Menu>
      </div>
      <div className="card">
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
                    <CreateQuestionModal closeModal={closeModal} />
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
      </div>
    </div>
  );
};

export default HomePage.wraps(Home);
