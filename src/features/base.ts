import { workspace, ExtensionContext } from 'coc.nvim'

const { nvim } = workspace
export class BaseProvider {
  constructor(private context: ExtensionContext) {
  }

  public async request(method: string, args: any[]): Promise<any> {
    return await nvim.callAsync('coc#jedi#request_async', [method, args])
  }

  public notify(method: string, args: any[]): void {
    nvim.call('coc#jedi#notify', [method, args], true)
  }

  public debug(message: any, ...args: any[]): void {
    this.context.logger.debug(message, ...args)
  }
}
