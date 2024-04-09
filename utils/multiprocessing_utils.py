import concurrent.futures
import traceback
import pandas as pd

"""
ThreadPoolExecutor/ProcessPoolExecutor --> Executor Object:
    fn submit
    fn map
    fn shutdown

Executor.submit --> Future objects:
    fn cancel
    fn cancelled
    fn running
    fn done
    fn result
    fn exception
    fn add_done_callback
    fn set_running_or_notify_cancel
    fn set_result
    fn set_exception
"""

threaded = True

# common args
max_workers = None

# only thread pool
thread_name_prefix = ''

# only process pool
mp_context = None
max_tasks_per_child = None

# for logging
log_func = print
log_at = 10_000

def run_in_parallel(fn_specs, threaded=threaded, max_workers=max_workers, thread_name_prefix=thread_name_prefix, mp_context=mp_context, max_tasks_per_child=max_tasks_per_child, log_at=log_at, log_func=log_func, log_progress = False):
    """
    Run function concurrently or paralelly

    Process Pool works fine on Linux. For Mac, import function you want to process from a separate module.

    Args:
        fn_specs : list : required
            List of Tuples where each tuple holds function in 1st place and arguments for function as a dictionary in second place.
        threaded : bool : optional : default - True
            If you want to run the function concurrently, set this to True. This will set the executor to ThreadPoolExecutor.
            If you want to spawn a separate process for each function set this to False. This will set the executor to ProcessPoolExecutor.
        max_workers: int : optional 
            Works for ThreadPoolExecutor and ProcessPoolExecutor differently. Refer Concurrent.Futures documentation for more details.
        thread_name_prefix : optional : default - ''
            Keyword Argument for ThreadPoolExecutor. Refer Concurrent.Futures documentation for more details.
        mp_context: optional : optional : default - None
            Keyword Argument for ProcessPoolExecutor. Refer Concurrent.Futures documentation for more details.
        max_tasks_per_child : optional : default - None
            Keyword Argument for ProcessPoolExecutor. Refer Concurrent.Futures documentation for more details.
    Returns:
        results : list
            list of tuples where 1st element of tuple will be argument passed to function and 2nd element will be output from the function
        exceptions : list
            list of tuples where 1st element of tuple will be argument passed to function, 2nd element will be Exception Name, 
            and 3rd element will be traceback

    """
    # executor_fn = concurrent.futures.ThreadPoolExecutor if threaded else concurrent.futures.ProcessPoolExecutor

    func_list = [i[0] for i in fn_specs]
    kwargs_list = [i[1] for i in fn_specs]
    len_func_list = len(func_list)

    if threaded:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix=thread_name_prefix) as executor:
            futures = {}
            results = []
            exceptions = []
            for fn, kwargs in zip(func_list,kwargs_list):
                futures.update({executor.submit(fn, **kwargs) : kwargs})
            for num_future, future in enumerate(concurrent.futures.as_completed(futures)):
                if (log_progress) & (num_future%log_at == 0):
                    log_func(f"Execution of {num_future}/{len_func_list} complete.")
                try:
                    result = future.result()
                    results.append((futures[future], result))
                except Exception as e:
                    exc = type(e).__name__
                    exceptions.append((futures[future],exc,traceback.format_exc()))
        return results, exceptions

    if not threaded:
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers, mp_context=mp_context) as executor:
            futures = {}
            results = []
            exceptions = []
            for fn, kwargs in zip(func_list,kwargs_list):
                futures.update({executor.submit(fn, **kwargs) : kwargs})
            for num_future, future in enumerate(concurrent.futures.as_completed(futures)):
                if (log_progress) & (num_future%log_at == 0):
                    log_func(f"Execution of {num_future}/{len_func_list} complete.")
                try:
                    result = future.result()
                    results.append((futures[future], result))
                except Exception as e:
                    exc = type(e).__name__
                    exceptions.append((futures[future],exc,traceback.format_exc()))
        return results, exceptions
    

def apply_on_series(df, func):
    return df.progress_apply(func)

def multicore_apply_by_chunks(df_st, func, max_chunks, max_workers = None, log_progress=False):
    max_workers = max_chunks if not max_workers else max_workers
    len_df = df_st.shape[0]
    n = len_df // max_chunks +1
    chunks = [df_st[i:i+n] for i in range(0,len_df,n)]
    fn_specs = []
    for i in chunks:
        fn_specs.append((apply_on_series, {"df" : i, 'func': func}))
    
    results, exceptions = run_in_parallel(fn_specs, threaded = False, max_workers = max_workers, log_at = 1, log_func = log_info, log_progress = log_progress)
    if len(exceptions) > 0 : print(exceptions[0][2])
    results = pd.concat(i[1] for i in results)
    del chunks
    del fn_specs
    del exceptions
    gc.collect()
    return results

pd.Series.multicore_apply_by_chunks = multicore_apply_by_chunks