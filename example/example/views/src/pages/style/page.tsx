import * as React from "react";
import * as StyleController from "./_server";
import { Dialog, Menu, MenuButton, MenuItem, MenuItems, Transition, TransitionChild, DialogPanel, DialogTitle, RadioGroup, Radio, Tab, TabList, TabPanel, TabPanels } from '@headlessui/react';
import { createServerPage } from "@/components/ServerPages";
import { LayoutPage } from "../layout";

const StylePage = createServerPage(StyleController);

const OptionsMenu = () => (
  <Menu as="div" className="relative inline-block text-left">
    <MenuButton className="btn btn-secondary">
      Options <span className="ml-2">&#9662;</span>
    </MenuButton>
    <MenuItems className="absolute right-0 mt-2 w-48 bg-white shadow-lg z-10 rounded-md">
      <MenuItem>
        <button className="block w-full text-left px-4 py-2 text-sm text-gray-700 rounded-md">
          Option 1
        </button>
      </MenuItem>
      <MenuItem>
        <button className="block w-full text-left px-4 py-2 text-sm text-gray-700 rounded-md">
          Option 2
        </button>
      </MenuItem>
    </MenuItems>
  </Menu>
);

export type Tab = {
  label: string;
  content: React.ReactNode;
};

export const Tabs = ({ tabs }: { tabs: Tab[] }) => (
  <Tab.Group>
    <TabList className="flex p-1 space-x-1 bg-gray-800 rounded-xl">
      {tabs.map((tab, index) => (
        <Tab key={index} className={({ selected }) => (selected ? 'bg-primary text-white shadow' : 'text-gray-400 hover:bg-primary hover:text-white') + ' rounded-xl px-3 py-2'}>
          {tab.label}
        </Tab>
      ))}
    </TabList>
    <TabPanels>
      {tabs.map((tab, index) => (
        <TabPanel key={index}>
          {tab.content}
        </TabPanel>
      ))}
    </TabPanels>
  </Tab.Group>
);

const Card = ({ title, text }) => (
  <div className="card-body">
    <h2 className="card-title">{title}</h2>
    <p className="card-text">{text}</p>
  </div>
);

const InputField = ({ label }) => (
  <>
    <label className="label">
      <span className="label-text">{label}</span>
    </label>
    <input type="text" className="input input-bordered" />
  </>
);

const RadioGroupField = ({ label, options }) => (
  <>
    <label className="label">
      <span className="label-text">{label}</span>
    </label>
    <RadioGroup className="space-y-2">
      {options.map(option => (
        <Radio key={option.value} value={option.value} className={({ checked }) => `${checked ? 'bg-primary text-white' : 'bg-white text-black'} relative rounded-lg shadow-md px-5 py-4 cursor-pointer flex focus:outline-none`}>
          {({ checked }) => (
            <>
              <div className="flex items-center justify-between w-full">
                <div className="flex items-center">
                  <div className="text-sm">
                    <RadioGroup.Label as="p" className={`font-medium ${checked ? 'text-white' : 'text-gray-900'}`}>
                      {option.label}
                    </RadioGroup.Label>
                  </div>
                </div>
                {checked && (
                  <div className="flex-shrink-0 text-white">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                  </div>
                )}
              </div>
            </>
          )}
        </Radio>
      ))}
    </RadioGroup>
  </>
);

const Modal = ({ isOpen, closeModal, title, content }) => (
  <Transition appear show={isOpen} as={React.Fragment}>
    <Dialog as="div" className="relative z-10" onClose={closeModal}>
      <TransitionChild
        as={React.Fragment}
        enter="ease-out duration-300"
        enterFrom="opacity-0"
        enterTo="opacity-100"
        leave="ease-in duration-200"
        leaveFrom="opacity-100"
        leaveTo="opacity-0"
      >
        <div className="fixed inset-0 bg-black bg-opacity-25" />
      </TransitionChild>
      <div className="fixed inset-0 overflow-y-auto">
        <div className="flex min-h-full items-center justify-center p-4 text-center">
          <TransitionChild
            as={React.Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0 scale-95"
            enterTo="opacity-100 scale-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100 scale-100"
            leaveTo="opacity-0 scale-95"
          >
            <DialogPanel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-gray-800 p-6 text-left align-middle shadow-xl transition-all">
              <DialogTitle as="h3" className="text-lg font-medium leading-6 text-white">
                {title}
              </DialogTitle>
              <div className="mt-2">
                <p className="text-sm text-gray-400">
                  {content}
                </p>
              </div>
              <div className="mt-4">
                <button type="button" className="btn btn-primary" onClick={closeModal}>
                  Close
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </Transition>
);

const Style = () => {
  const { user } = LayoutPage.useContext();
  const [isOpen, setIsOpen] = React.useState(false);

  const openModal = () => setIsOpen(true);
  const closeModal = () => setIsOpen(false);

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl">Style</h1>
      </div>
      <div className="mb-4">
        <OptionsMenu />
      </div>
      <div className="mb-4">
        <Tabs tabs={[
          { label: "Tab 1", content: <p className="text-sm text-gray-400">Content for Tab 1</p> },
          { label: "Tab 2", content: <p className="text-sm text-gray-400">Content for Tab 2</p> }
        ]} />
      </div>
      <div className="card mb-4">
        <Card title="Card Title" text="This is some text within a card body." />
      </div>
      <div className="form-control mb-4">
        <InputField label="Input Label" />
      </div>
      <div className="form-control mb-4">
        <RadioGroupField label="Radio Group" options={[
          { value: "option1", label: "Option 1" },
          { value: "option2", label: "Option 2" }
        ]} />
      </div>
      <div className="flex justify-end space-x-2">
        <button type="button" onClick={openModal} className="btn btn-secondary">Open Modal</button>
        <button type="button" className="btn btn-primary">Submit</button>
      </div>
      <Modal isOpen={isOpen} closeModal={closeModal} title="Modal Title" content="Your modal content goes here." />
    </div>
  );
};

export default StylePage.wraps(Style);
