import React from 'react';
import {useForm} from 'react-hook-form';
import {useServer} from './_server';
import {handleFormSubmit} from "@/components/utils";

type LoginForm = {
  username: string,
  password: string
}

/* Floating center card with a login form*/
export default function LoginPage() {
  const server = useServer();
  const form = useForm<LoginForm>();
  return (
    <div className={"flex justify-center items-center h-full"}>
      <div className={"w-96 p-4 bg-base-100 rounded-xl"}>
        <h1 className={"text-3xl font-bold text-accent pb-2"}>Login</h1>
        <form className={"flex flex-col gap-4"}
              onSubmit={handleFormSubmit(form, server.login, {onSuccess: () => window.location.pathname = '/'})}>
          <input type={"text"} placeholder={"Username"}
                 className={"input input-primary"} {...form.register('username')}/>
          <input type={"password"} placeholder={"Password"}
                 className={"input input-primary"} {...form.register('password')}/>
          {form.formState.errors.root?.error &&
              <p className={"text-error"}>{form.formState.errors.root.error.message}</p>}
          <button type={"submit"} className={"btn btn-primary"}>Login</button>
        </form>
      </div>
    </div>
  );
}