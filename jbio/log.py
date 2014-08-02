

from functional import fpass

def logger(output_fh):
    
    if not output_fh:
        return fpass

    def _log(msg):
        '''Logs to output_fh'''
        output_fh.write(msg)
        output_fh.write("\n")
    
    return _log
